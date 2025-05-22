import secrets
import httpx
from uuid import UUID

from app.models.sensor_node import TTNKeys
from app.config import settings
from app.services.ttn.ttn_service_base import TtnServiceBase

class TtnServiceReal(TtnServiceBase):
    
    def __init__(self):
        self.app_id = settings.TTN_APP_ID
        api_key = settings.TTN_API_KEY
        if api_key is None:
            raise ValueError("TTN_API_KEY must be set as an environment variable in order to use the TTN service.")
        
        self.base_url = "https://eu1.cloud.thethings.network/api/v3"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    
    async def create_device(self, sensor_node_id: UUID) -> TTNKeys:
        device_id = str(sensor_node_id)
        dev_eui = self._random_hex(8)
        join_eui = "0000000000000000"
        app_key = self._random_hex(16)

        async with httpx.AsyncClient() as client:

            # === Schritt 1: Identity Server ===
            is_url = f"{self.base_url}/applications/{self.app_id}/devices"
            identity_payload = {
                "end_device": {
                    "ids": {
                        "device_id": device_id,
                        "dev_eui": dev_eui,
                        "join_eui": join_eui
                    },
                    "version_ids": {
                        "brand_id": "heltec",
                        "model_id": "cubecell-dev-board-class-a-otaa",
                        "firmware_version": "1.0",
                        "band_id": "EU_863_870_TTN"
                    },
                    "network_server_address": "eu1.cloud.thethings.network",
                    "application_server_address": "eu1.cloud.thethings.network",
                    "join_server_address": "eu1.cloud.thethings.network"
                },
                "field_mask": {
                    "paths": [
                        "ids.dev_eui",
                        "ids.join_eui",
                        "network_server_address",
                        "application_server_address",
                        "join_server_address",
                        "version_ids.brand_id",
                        "version_ids.model_id",
                        "version_ids.firmware_version",
                        "version_ids.band_id"
                    ]
                }
            }
            is_resp = await client.post(is_url, json=identity_payload, headers=self.headers)
            if not is_resp.is_success:
                raise Exception(f"Identity Server error: {is_resp.status_code} – {is_resp.text}")

            # === Schritt 2: Join Server ===
            js_url = f"{self.base_url}/js/applications/{self.app_id}/devices/{device_id}"
            join_payload = {
                "end_device": {
                    "ids": {
                        "device_id": device_id,
                        "dev_eui": dev_eui,
                        "join_eui": join_eui
                    },
                    "network_server_address": "eu1.cloud.thethings.network",
                    "application_server_address": "eu1.cloud.thethings.network",
                    "root_keys": {
                        "app_key": {
                            "key": app_key
                        }
                    }
                },
                "field_mask": {
                    "paths": [
                        "network_server_address",
                        "application_server_address",
                        "ids.device_id",
                        "ids.dev_eui",
                        "ids.join_eui",
                        "root_keys.app_key.key"
                    ]
                }
            }
            js_resp = await client.put(js_url, json=join_payload, headers=self.headers)
            if not js_resp.is_success:
                raise Exception(f"Join Server error: {js_resp.status_code} – {js_resp.text}")

            # === Schritt 3: Network Server ===
            ns_url = f"{self.base_url}/ns/applications/{self.app_id}/devices/{device_id}"
            ns_payload = {
                "end_device": {
                    "supports_join": True,
                    "ids": {
                        "device_id": device_id,
                        "dev_eui": dev_eui,
                        "join_eui": join_eui
                    },
                    "lorawan_version": "MAC_V1_0_2",
                    "lorawan_phy_version": "PHY_V1_0_2_REV_B",
                    "frequency_plan_id": "EU_863_870_TTN"
                },
                "field_mask": {
                    "paths": [
                        "supports_join",
                        "lorawan_version",
                        "ids.device_id",
                        "ids.dev_eui",
                        "ids.join_eui",
                        "lorawan_phy_version",
                        "frequency_plan_id"
                    ]
                }
            }
            ns_resp = await client.put(ns_url, json=ns_payload, headers=self.headers)
            if not ns_resp.is_success:
                raise Exception(f"Network Server error: {ns_resp.status_code} – {ns_resp.text}")

            # === Schritt 4: Application Server ===
            as_url = f"{self.base_url}/as/applications/{self.app_id}/devices/{device_id}"
            as_payload = {
                "end_device": {
                    "ids": {
                        "device_id": device_id,
                        "dev_eui": dev_eui,
                        "join_eui": join_eui
                    }
                },
                "field_mask": {
                    "paths": [
                        "ids.device_id",
                        "ids.dev_eui",
                        "ids.join_eui"
                    ]
                }
            }
            as_resp = await client.put(as_url, json=as_payload, headers=self.headers)
            if not as_resp.is_success:
                raise Exception(f"Application Server error: {as_resp.status_code} – {as_resp.text}")

        return TTNKeys(
            app_key=app_key,
            dev_eui=dev_eui,
            join_eui=join_eui
        )

    async def delete_device(self, sensor_node_id: UUID) -> None:

        async with httpx.AsyncClient() as client:
            # === Schritt 1: Application Server ===
            as_url = f"{self.base_url}/as/applications/{self.app_id}/devices/{sensor_node_id}"
            as_resp = await client.delete(as_url, headers=self.headers)
            if not as_resp.is_success:
                raise Exception(f"Application Server error: {as_resp.status_code} – {as_resp.text}")

            # === Schritt 2: Network Server ===
            ns_url = f"{self.base_url}/ns/applications/{self.app_id}/devices/{sensor_node_id}"
            ns_resp = await client.delete(ns_url, headers=self.headers)
            if not ns_resp.is_success:
                raise Exception(f"Network Server error: {ns_resp.status_code} – {ns_resp.text}")

            # === Schritt 3: Join Server ===
            js_url = f"{self.base_url}/js/applications/{self.app_id}/devices/{sensor_node_id}"
            js_resp = await client.delete(js_url, headers=self.headers)
            if not js_resp.is_success:
                raise Exception(f"Join Server error: {js_resp.status_code} – {js_resp.text}")

            # === Schritt 4: Identity Server ===
            is_url = f"{self.base_url}/applications/{self.app_id}/devices/{sensor_node_id}"
            is_resp = await client.delete(is_url, headers=self.headers)
            if not is_resp.is_success:
                raise Exception(f"Identity Server error: {is_resp.status_code} – {is_resp.text}")

    def build_device_link(self, sensor_node_id: UUID) -> str:
        return f"https://eu1.cloud.thethings.network/console/applications/{self.app_id}/devices/{sensor_node_id}"

    def _random_hex(self, length_bytes: int) -> str:
        return secrets.token_hex(length_bytes).upper()