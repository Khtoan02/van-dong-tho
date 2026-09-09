#!/usr/bin/env python
"""Render exact CSS viewports through an existing Chrome CDP port.

Requires: websocket-client
Chrome must already be running with --remote-debugging-port.
"""

import argparse
import base64
import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

import websocket


def open_target(cdp_base: str) -> dict:
    endpoint = cdp_base.rstrip("/") + "/json/new?" + urllib.parse.quote("about:blank", safe=":/")
    request = urllib.request.Request(endpoint, method="PUT")
    with urllib.request.urlopen(request, timeout=10) as response:
        return json.load(response)


def render(cdp_base: str, url: str, width: int, height: int, output: Path) -> dict:
    target = open_target(cdp_base)
    socket = websocket.create_connection(target["webSocketDebuggerUrl"], timeout=15)
    sequence = 0

    def call(method: str, params: dict | None = None) -> dict:
        nonlocal sequence
        sequence += 1
        current = sequence
        socket.send(json.dumps({"id": current, "method": method, "params": params or {}}))
        while True:
            message = json.loads(socket.recv())
            if message.get("id") != current:
                continue
            if "error" in message:
                raise RuntimeError(message["error"])
            return message.get("result", {})

    try:
        call("Page.enable")
        call("Runtime.enable")
        call(
            "Emulation.setDeviceMetricsOverride",
            {
                "width": width,
                "height": height,
                "deviceScaleFactor": 1,
                "mobile": width < 700,
                "screenWidth": width,
                "screenHeight": height,
            },
        )
        call("Page.navigate", {"url": url})

        deadline = time.time() + 20
        while time.time() < deadline:
            state = call(
                "Runtime.evaluate",
                {"expression": "document.readyState", "returnByValue": True},
            )["result"]["value"]
            if state == "complete":
                break
            time.sleep(0.1)
        else:
            raise TimeoutError(f"Page did not finish loading: {url}")

        time.sleep(0.5)
        capture = call(
            "Page.captureScreenshot",
            {"format": "png", "captureBeyondViewport": False},
        )
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(base64.b64decode(capture["data"]))

        metrics = call(
            "Runtime.evaluate",
            {
                "expression": "({innerWidth,innerHeight,clientWidth:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,scrollHeight:document.documentElement.scrollHeight})",
                "returnByValue": True,
            },
        )["result"]["value"]
        metrics["horizontalOverflow"] = metrics["scrollWidth"] > metrics["clientWidth"]
        metrics["file"] = str(output.resolve())
        return metrics
    finally:
        socket.close()


def parse_viewport(value: str) -> tuple[str, int, int]:
    try:
        name, dimensions = value.split(":", 1)
        width, height = dimensions.lower().split("x", 1)
        return name, int(width), int(height)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("Use NAME:WIDTHxHEIGHT") from exc


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--cdp", default="http://127.0.0.1:9333")
    parser.add_argument("--out-dir", type=Path, default=Path("renders"))
    parser.add_argument(
        "--viewport",
        action="append",
        type=parse_viewport,
        required=True,
        help="Repeatable NAME:WIDTHxHEIGHT, e.g. mobile:390x844",
    )
    args = parser.parse_args()

    results = {}
    for name, width, height in args.viewport:
        output = args.out_dir / f"{name}.png"
        results[name] = render(args.cdp, args.url, width, height, output)
    print(json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
