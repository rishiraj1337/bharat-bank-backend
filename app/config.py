import os
import json
import logging
from typing import Any, Dict, Optional
import xmltodict

CONFIG_PATH = os.environ.get("MOCK_CONFIG_PATH", "mock_config.json")
logger = logging.getLogger("mock_cbs.config")


class MockConfigManager:
    def __init__(self, config_file: str = CONFIG_PATH):
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, "r", encoding="utf-8") as f:
                    self.config = json.load(f)
                logger.info(f"Loaded mock configuration from {self.config_file}")
            except Exception as e:
                logger.error(f"Error loading {self.config_file}: {e}")
                self.config = self._default_config()
        else:
            logger.warning(f"Config file {self.config_file} not found. Using defaults.")
            self.config = self._default_config()
            self.save_config()
        return self.config

    def save_config(self) -> bool:
        try:
            with open(self.config_file, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save config: {e}")
            return False

    def get_endpoint_config(self, endpoint_key: str) -> Dict[str, Any]:
        endpoints = self.config.get("endpoints", {})
        if endpoint_key in endpoints:
            return endpoints[endpoint_key]
        return {
            "mode": self.config.get("settings", {}).get("default_mode", "static"),
            "status_code": 200,
            "delay_ms": self.config.get("settings", {}).get("default_delay_ms", 0),
            "data": {}
        }

    def update_endpoint_config(self, endpoint_key: str, new_config: Dict[str, Any]) -> None:
        if "endpoints" not in self.config:
            self.config["endpoints"] = {}
        self.config["endpoints"][endpoint_key] = new_config
        self.save_config()

    def _default_config(self) -> Dict[str, Any]:
        return {
            "settings": {
                "default_mode": "static",
                "default_delay_ms": 0,
                "log_to_file": True,
                "log_file_path": "logs/mock_server.log"
            },
            "endpoints": {}
        }


config_manager = MockConfigManager()


def dict_to_xml(root_tag: str, data: Dict[str, Any]) -> str:
    """Converts a python dictionary into a formatted XML string."""
    try:
        wrapped = {root_tag: data}
        return xmltodict.unparse(wrapped, pretty=True)
    except Exception as e:
        # Fallback simple XML generator
        xml_lines = [f"<{root_tag}>"]
        for k, v in data.items():
            xml_lines.append(f"    <{k}>{v}</{k}>")
        xml_lines.append(f"</{root_tag}>")
        return "\n".join(xml_lines)


def wrap_cbs_envelope(body_tag: str, body_data: Dict[str, Any], correlation_id: str = "CORR123456", message_id: str = "MSG20260904001", status: str = "SUCCESS") -> Dict[str, Any]:
    from datetime import datetime
    return {
        "CBSResponse": {
            "Header": {
                "MessageId": message_id,
                "CorrelationId": correlation_id,
                "Status": status,
                "ResponseTimestamp": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S")
            },
            "Body": {
                body_tag: body_data
            }
        }
    }
