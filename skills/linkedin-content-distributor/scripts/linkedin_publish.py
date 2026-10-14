#!/usr/bin/env python3
"""Prepare and publish LinkedIn member posts without persisting OAuth tokens in files."""

from __future__ import annotations

import argparse
import getpass
import hashlib
import json
import os
import ssl
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


API_ROOT = "https://api.linkedin.com"
KEYCHAIN_TIMEOUT_SECONDS = 60


class LinkedInError(RuntimeError):
    pass


def read_text(path: str) -> str:
    value = Path(path).read_text(encoding="utf-8").strip()
    if not value:
        raise LinkedInError("帖子文案不能为空")
    return value


def validate_version(value: str) -> str:
    if len(value) != 6 or not value.isdigit():
        raise LinkedInError("LinkedIn-Version 必须采用 YYYYMM 格式")
    return value


def keychain_token(service: str, account: str) -> str:
    env_token = os.environ.get("LINKEDIN_ACCESS_TOKEN", "").strip()
    if env_token:
        return env_token
    if sys.platform != "darwin":
        raise LinkedInError("非 macOS 环境请通过 LINKEDIN_ACCESS_TOKEN 提供令牌")
    searches = (
        ["security", "find-generic-password", "-s", service, "-a", account, "-w"],
        ["security", "find-generic-password", "-l", service, "-a", account, "-w"],
    )
    for command in searches:
        try:
            result = subprocess.run(
                command,
                check=False,
                capture_output=True,
                text=True,
                timeout=KEYCHAIN_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as exc:
            raise LinkedInError(
                "读取 macOS 钥匙串超时；请在系统提示中点按“允许”或“始终允许”后重试"
            ) from exc
        token = result.stdout.strip()
        if result.returncode == 0 and token:
            return token
    raise LinkedInError("macOS 钥匙串中未找到 LinkedIn Access Token")


def store_keychain_token(service: str, account: str) -> str:
    if sys.platform != "darwin":
        raise LinkedInError("store-token 仅支持 macOS 钥匙串")
    token = getpass.getpass("粘贴 LinkedIn Access Token（输入不会显示）: ").strip()
    if not token:
        raise LinkedInError("未输入 Access Token")
    try:
        result = subprocess.run(
            [
                "security",
                "add-generic-password",
                "-U",
                "-s",
                service,
                "-a",
                account,
                "-w",
                token,
            ],
            check=False,
            capture_output=True,
            text=True,
            timeout=KEYCHAIN_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise LinkedInError(
            "写入 macOS 钥匙串超时；请处理系统授权提示后重试"
        ) from exc
    if result.returncode != 0:
        raise LinkedInError("写入 macOS 钥匙串失败")
    print(json.dumps({"status": "stored", "service": service, "account": account}, ensure_ascii=False))
    return token


def ssl_context() -> ssl.SSLContext:
    if sys.platform == "darwin":
        system_bundle = Path("/etc/ssl/cert.pem")
        if system_bundle.is_file():
            return ssl.create_default_context(cafile=str(system_bundle))
    return ssl.create_default_context()


def api_request(method: str, url: str, token: str, *, version: str | None = None, body: dict | None = None):
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if version:
        headers["Linkedin-Version"] = validate_version(version)
        headers["X-Restli-Protocol-Version"] = "2.0.0"
    data = None
    if body is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(body, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30, context=ssl_context()) as response:
            raw = response.read().decode("utf-8")
            parsed = json.loads(raw) if raw else None
            return response.status, dict(response.headers.items()), parsed
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise LinkedInError(f"LinkedIn API 返回 HTTP {exc.code}: {detail[:1000]}") from exc
    except urllib.error.URLError as exc:
        raise LinkedInError(f"LinkedIn API 网络错误: {exc.reason}") from exc


def resolve_author_urn(token: str, explicit: str | None) -> str:
    if explicit:
        if not explicit.startswith("urn:li:person:"):
            raise LinkedInError("--author-urn 必须采用 urn:li:person:{id} 格式")
        return explicit
    _, _, profile = api_request("GET", f"{API_ROOT}/v2/userinfo", token)
    member_id = (profile or {}).get("sub")
    if not member_id:
        raise LinkedInError("无法取得成员 ID；请使用含 openid profile 的令牌，或传入 --author-urn")
    return f"urn:li:person:{member_id}"


def check_connection(args: argparse.Namespace) -> None:
    token = keychain_token(args.keychain_service, args.keychain_account)
    author_urn = resolve_author_urn(token, None)
    print(json.dumps({"status": "connected", "author_urn": author_urn}, ensure_ascii=False))


def setup(args: argparse.Namespace) -> None:
    print("首次配置：请粘贴包含 openid、profile、w_member_social 权限的 Access Token。")
    token = store_keychain_token(args.keychain_service, args.keychain_account)
    author_urn = resolve_author_urn(token, None)
    print(
        json.dumps(
            {
                "status": "ready",
                "author_urn": author_urn,
                "next_step": "使用 prepare 生成预览；获得用户确认后再使用 publish --approve",
            },
            ensure_ascii=False,
        )
    )


def build_payload(args: argparse.Namespace, author_urn: str) -> dict:
    payload = {
        "author": author_urn,
        "commentary": read_text(args.text_file),
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }
    if args.article_url:
        article = {"source": args.article_url}
        if args.article_title:
            article["title"] = args.article_title
        if args.article_description:
            article["description"] = args.article_description
        payload["content"] = {"article": article}
    return payload


def fingerprint(payload: dict) -> str:
    material = json.dumps(
        {
            "author": payload["author"],
            "commentary": payload["commentary"].strip(),
            "source": payload.get("content", {}).get("article", {}).get("source", ""),
        },
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(material.encode("utf-8")).hexdigest()


def existing_record(path: Path, value: str) -> dict | None:
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record.get("content_fingerprint") == value and record.get("publish_status") in {
            "published_and_verified",
            "published_but_unverified",
        }:
            return record
    return None


def append_record(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def publish(args: argparse.Namespace) -> None:
    if not args.approve:
        raise LinkedInError("发布属于外部写入；确认最终预览后必须显式添加 --approve")
    token = keychain_token(args.keychain_service, args.keychain_account)
    author_urn = resolve_author_urn(token, args.author_urn)
    payload = build_payload(args, author_urn)
    digest = fingerprint(payload)
    record_path = Path(args.record_file).expanduser().resolve()
    duplicate = existing_record(record_path, digest)
    if duplicate:
        raise LinkedInError(f"检测到相同内容已经发布，帖子 ID: {duplicate.get('linkedin_post_id', 'unknown')}")

    status, headers, _ = api_request(
        "POST",
        f"{API_ROOT}/rest/posts",
        token,
        version=args.linkedin_version,
        body=payload,
    )
    post_id = headers.get("x-restli-id") or headers.get("X-RestLi-Id")
    if status != 201 or not post_id:
        raise LinkedInError("API 未返回可验证的 LinkedIn 帖子 ID")

    verification = "published_but_unverified"
    try:
        encoded = urllib.parse.quote(post_id, safe="")
        read_status, _, published = api_request(
            "GET",
            f"{API_ROOT}/rest/posts/{encoded}",
            token,
            version=args.linkedin_version,
        )
        if read_status == 200 and (published or {}).get("author") == author_urn:
            verification = "published_and_verified"
    except LinkedInError:
        pass

    public_url = f"https://www.linkedin.com/feed/update/{post_id}/"
    record = {
        "content_fingerprint": digest,
        "publish_status": verification,
        "linkedin_post_id": post_id,
        "linkedin_post_url": public_url,
        "published_at": datetime.now(timezone.utc).isoformat(),
        "source_url": args.article_url,
        "target": author_urn,
    }
    append_record(record_path, record)
    print(json.dumps(record, ensure_ascii=False, indent=2))


def prepare(args: argparse.Namespace) -> None:
    author = args.author_urn or "urn:li:person:<通过 openid profile 自动取得>"
    payload = build_payload(args, author)
    print(
        json.dumps(
            {
                "mode": "prepare-only",
                "linkedin_version": validate_version(args.linkedin_version),
                "payload": payload,
                "content_fingerprint": fingerprint(payload),
            },
            ensure_ascii=False,
            indent=2,
        )
    )


def add_content_arguments(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--text-file", required=True, help="UTF-8 帖子文案文件")
    parser.add_argument("--article-url")
    parser.add_argument("--article-title")
    parser.add_argument("--article-description")
    parser.add_argument("--author-urn", help="已验证的 urn:li:person:{id}；省略时通过 userinfo 获取")
    parser.add_argument("--linkedin-version", required=True, help="LinkedIn Marketing API 版本，格式 YYYYMM")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="安全准备或发布 LinkedIn 个人账号帖子")
    subparsers = parser.add_subparsers(dest="command", required=True)

    store = subparsers.add_parser("store-token", help="交互式保存 Access Token 到 macOS 钥匙串")
    store.add_argument("--keychain-service", default="codex-linkedin-access-token")
    store.add_argument("--keychain-account", default="personal")

    onboarding = subparsers.add_parser("setup", help="首次配置：保存令牌并立即验证个人账号连接")
    onboarding.add_argument("--keychain-service", default="codex-linkedin-access-token")
    onboarding.add_argument("--keychain-account", default="personal")

    preview = subparsers.add_parser("prepare", help="生成负载和内容指纹，不访问 LinkedIn")
    add_content_arguments(preview)

    check = subparsers.add_parser("check", help="验证钥匙串令牌和 LinkedIn 个人身份，不发布")
    check.add_argument("--keychain-service", default="codex-linkedin-access-token")
    check.add_argument("--keychain-account", default="personal")

    send = subparsers.add_parser("publish", help="发布并尽力读回验证")
    add_content_arguments(send)
    send.add_argument("--keychain-service", default="codex-linkedin-access-token")
    send.add_argument("--keychain-account", default="personal")
    send.add_argument("--record-file", required=True, help="JSONL 分发记录路径")
    send.add_argument("--approve", action="store_true", help="确认已经批准本次准确的目标和最终内容")
    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()
        if args.command == "store-token":
            store_keychain_token(args.keychain_service, args.keychain_account)
        elif args.command == "setup":
            setup(args)
        elif args.command == "prepare":
            prepare(args)
        elif args.command == "check":
            check_connection(args)
        elif args.command == "publish":
            publish(args)
        return 0
    except (LinkedInError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"status": "failed", "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
