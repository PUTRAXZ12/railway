#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import json
import base64
import binascii
import time
import warnings
warnings.filterwarnings("ignore")
import requests
requests.packages.urllib3.disable_warnings()
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf import descriptor_pool, message_factory

# ---------- Colours ----------
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    BOLD = Style.BRIGHT
    RESET = Style.RESET_ALL
except ImportError:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

# ---------- Protobuf ----------
mYdEsCrIpToR = b'\n\x08my.proto"\xae\t\n\x08GameData\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x14\n\x0cgame_version\x18\x05 \x01(\x05\x12\x14\n\x0cversion_code\x18\x07 \x01(\t\x12\x0f\n\x07os_info\x18\x08 \x01(\t\x12\x13\n\x0bdevice_type\x18\t \x01(\t\x12\x18\n\x10network_provider\x18\n \x01(\t\x12\x17\n\x0fconnection_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\x05\x12\x15\n\rscreen_height\x18\r \x01(\x05\x12\x0b\n\x03dpi\x18\x0e \x01(\t\x12\x10\n\x08cpu_info\x18\x0f \x01(\t\x12\x11\n\ttotal_ram\x18\x10 \x01(\x05\x12\x10\n\x08gpu_name\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x0f\n\x07user_id\x18\x13 \x01(\t\x12\x12\n\nip_address\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x15\n\rplatform_type\x18\x17 \x01(\x05\x12\x1a\n\x12device_form_factor\x18\x18 \x01(\t\x12\x14\n\x0cdevice_model\x18\x19 \x01(\t\x12\x14\n\x0caccess_token\x18\x1d \x01(\t\x12\x18\n\x10unknown_field_30\x18\x1e \x01(\x05\x12"\n\x1asecondary_network_provider\x18) \x01(\t\x12!\n\x19secondary_connection_type\x18* \x01(\t\x12\x11\n\tunique_id\x18\x39 \x01(\t\x12\x10\n\x08field_60\x18< \x01(\x05\x12\x10\n\x08field_61\x18= \x01(\x05\x12\x10\n\x08field_62\x18> \x01(\x05\x12\x10\n\x08field_63\x18? \x01(\x05\x12\x10\n\x08field_64\x18@ \x01(\x05\x12\x10\n\x08field_65\x18A \x01(\x05\x12\x10\n\x08field_66\x18B \x01(\x05\x12\x10\n\x08field_67\x18C \x01(\x05\x12\x10\n\x08field_70\x18F \x01(\x05\x12\x10\n\x08field_73\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x10\n\x08field_76\x18L \x01(\x05\x12\x10\n\x08apk_info\x18M \x01(\t\x12\x10\n\x08field_78\x18N \x01(\x05\x12\x10\n\x08field_79\x18O \x01(\x05\x12\x17\n\x0fos_architecture\x18Q \x01(\t\x12\x14\n\x0cbuild_number\x18S \x01(\t\x12\x10\n\x08field_85\x18U \x01(\x05\x12\x18\n\x10graphics_backend\x18V \x01(\t\x12\x19\n\x11max_texture_units\x18W \x01(\x05\x12\x15\n\rrendering_api\x18X \x01(\x05\x12\x18\n\x10encoded_field_89\x18Y \x01(\t\x12\x10\n\x08field_92\x18\\ \x01(\x05\x12\x13\n\x0bmarketplace\x18] \x01(\t\x12\x16\n\x0eencryption_key\x18^ \x01(\t\x12\x15\n\rtotal_storage\x18_ \x01(\x05\x12\x10\n\x08field_97\x18a \x01(\x05\x12\x10\n\x08field_98\x18b \x01(\x05\x12\x10\n\x08field_99\x18c \x01(\t\x12\x11\n\tfield_100\x18d \x01(\tb\x06proto3'

oUtPuTdEsCrIpToR = b'\n\x13jwt_generator.proto"\xd2\x02\n\nGarena_420\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05place\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\n\n\x02id\x18\t \x01(\x05\x12\x0b\n\x03api\x18\n \x01(\t\x12\x0e\n\x06number\x18\x0c \x01(\x05\x12\x1e\n\tGarena420\x18\x0f \x01(\x0b\x32\x0b.Garena_420\x12\x0c\n\x04area\x18\x10 \x01(\t\x12\x11\n\tmain_area\x18\x12 \x01(\t\x12\x0c\n\x04city\x18\x13 \x01(\t\x12\x0c\n\x04name\x18\x14 \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0e\n\x06binary\x18\x16 \x01(\x0c\x12\x13\n\x0bbinary_data\x18\x17 \x01(\x0c\x1a"\n\x12Decrypted_Payloads\x12\x0c\n\x04type\x18\x01 \x01(\x05b\x06proto3'

pOoL = descriptor_pool.Default()
pOoL.AddSerializedFile(mYdEsCrIpToR)
pOoL.AddSerializedFile(oUtPuTdEsCrIpToR)

gAmEdAtA = message_factory.GetMessageClass(pOoL.FindMessageTypeByName('GameData'))
gArEnA420 = message_factory.GetMessageClass(pOoL.FindMessageTypeByName('Garena_420'))

# ---------- AES ----------
AES_KEY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
AES_IV  = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

MAJOR_LOGIN_URL = "https://loginbp.ggblueshark.com/MajorLogin"

def encrypt(data):
    cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
    return cipher.encrypt(pad(data, AES.block_size))

def decrypt(data):
    if len(data) % 16 != 0:
        return data
    try:
        cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)
        return unpad(cipher.decrypt(data), AES.block_size)
    except:
        return data

# ---------- Protobuf Parser ----------
def write_varint(value):
    result = []
    while value > 127:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value)
    return bytes(result)

def read_varint(data, offset):
    result = 0
    shift = 0
    while True:
        byte = data[offset]
        result |= (byte & 0x7F) << shift
        offset += 1
        if not (byte & 0x80):
            break
        shift += 7
    return result, offset

def parse_protobuf(data):
    result = {}
    offset = 0
    while offset < len(data):
        tag, offset = read_varint(data, offset)
        field = tag >> 3
        wire = tag & 0x7
        if wire == 0:
            value, offset = read_varint(data, offset)
            result[field] = (0, value)
        elif wire == 2:
            length, offset = read_varint(data, offset)
            value = data[offset:offset+length]
            offset += length
            try:
                str_val = value.decode('utf-8')
                result[field] = (2, str_val, value)
            except:
                result[field] = (2, value)
        else:
            break
    return result

# ---------- Template ----------
TEMPLATE_FIELDS = {
    3: "TIMESTAMP_PLACEHOLDER",
    4: "free fire",
    5: 1,
    7: "1.132.1",
    8: "Android OS 13 / API-33 (TQ1A.230205.002/9471150)",
    9: "Handheld",
    10: "45412",
    11: "WIFI",
    12: 1280,
    13: 720,
    14: "320",
    15: "ARM64 FP ASIMD AES | 2352 | 8",
    16: 5459,
    17: "Mali-G610",
    18: "OpenGL ES 3.2 v1.g18p0-01eac0.2d5e200a1514bdef1a4909db66e37e28",
    19: "Google|27d148dd-62e3-4754-a014-0f6d129cac10",
    20: "162.128.224.29",
    21: "en",
    23: 4,
    24: "Handheld",
    25: "google Pixel 5a",
    26: "IND",
    30: 1,
    41: "45412",
    42: "WIFI",
    57: "1ac4b80ecf0478a44203bf8fac6120f5",
    60: 28294,
    61: 24413,
    62: 2427,
    64: 24541,
    65: 28294,
    66: 24541,
    67: 28294,
    73: 1,
    74: "/data/app/~~3bD6d9uj0WBMEp8yVNFIYw==/com.dts.freefireth-sv3hVa-3_lWk4ccFYwXvAA==/lib/arm64",
    76: 2,
    77: "7428b253defc164018c604a1ebbfebdf|/data/app/~~3bD6d9uj0WBMEp8yVNFIYw==/com.dts.freefireth-sv3hVa-3_lWk4ccFYwXvAA==/base.apk",
    78: 2,
    79: 2,
    81: "64",
    83: "2019121229",
    85: 3,
    86: "OpenGLES3",
    87: 8191,
    88: 4,
    92: 26023,
    93: "android_max",
    94: "KqSHTylre+Z3Wsu5pH+Bk6lZgeLV/3MWoDWWUu2cO6GN2j4M0HViGz3fPN+0mcA1QEgStJkmxdJoDtq98WXjLre7tZuHEiWy cG+WOL0iH8njNkG",
    96: '{"cur_rate":null,"support_etc2":true}',
    98: 1,
    99: "4",
    100: "4",
    102: {}
}

def build_modified_game(original_open_id, original_access_token, platform):
    game = gAmEdAtA()
    fields_by_num = gAmEdAtA.DESCRIPTOR.fields_by_number
    for field_num, value in TEMPLATE_FIELDS.items():
        if field_num == 3:
            value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        elif field_num == 23 or field_num == 99 or field_num == 100:
            value = str(platform)
        field = fields_by_num.get(field_num)
        if field is None:
            continue
        if field.type == field.TYPE_STRING:
            setattr(game, field.name, str(value))
        elif field.type in (field.TYPE_INT32, field.TYPE_INT64,
                            field.TYPE_UINT32, field.TYPE_UINT64,
                            field.TYPE_SINT32, field.TYPE_SINT64):
            setattr(game, field.name, int(value))
        elif field.type == field.TYPE_BYTES:
            if isinstance(value, str):
                try:
                    value = binascii.unhexlify(value)
                except:
                    value = value.encode()
            setattr(game, field.name, value)
        elif field.type == field.TYPE_BOOL:
            setattr(game, field.name, bool(value))
        else:
            setattr(game, field.name, value)

    game.open_id = original_open_id
    game.access_token = original_access_token
    return game

def forward_majorlogin_request(modified_game):
    serialized = modified_game.SerializeToString()
    encrypted = encrypt(serialized)
    headers = {
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
        "Content-Type": "application/octet-stream",
        "X-Unity-Version": "2018.4.11f1",
        "X-GA": "v1 1",
        "ReleaseVersion": "OB55"
    }
    resp = requests.post(MAJOR_LOGIN_URL, data=encrypted, headers=headers, verify=False, timeout=10)
    return resp.content if resp.status_code == 200 else None

# ---------- HTTP Handler ----------
class DynamicHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self._handle()
    def do_POST(self):
        self._handle()
    def _handle(self):
        path = self.path
        if path == "/Ping":
            self.send_response(200)
            self.send_header('Content-Length', '0')
            self.send_header('Connection', 'close')
            self.end_headers()
            return
        if path == "/MajorLogin":
            self._handle_majorlogin()
            return
        self.send_response(404)
        self.send_header('Content-Length', '0')
        self.send_header('Connection', 'close')
        self.end_headers()

    def _handle_majorlogin(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length else b''
        try:
            decrypted = decrypt(body)
            decoded_fields = parse_protobuf(decrypted)
        except Exception as e:
            print(f"{RED}        Error decrypting/parsing request: {e}{RESET}")
            self.send_response(500)
            self.end_headers()
            return

        open_id = decoded_fields.get(22, (None,))[1] if 22 in decoded_fields else None
        access_token = decoded_fields.get(29, (None,))[1] if 29 in decoded_fields else None

        if not open_id or not access_token:
            print(f"{RED}        Missing open_id or access_token. Forwarding original.{RESET}")
            try:
                resp = requests.post(MAJOR_LOGIN_URL, data=body, headers=dict(self.headers), verify=False, timeout=10)
                content = resp.content
                self.send_response(resp.status_code)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', len(content))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print(f"{RED}        Error: {e}{RESET}")
                self.send_response(500)
                self.end_headers()
            return

        print(f"{CYAN}        Intercepted MajorLogin – open_id: {open_id}{RESET}")
        print(f"{CYAN}        access_token: {access_token[:20]}...{RESET}")

        platforms = [4, 8, 3, 6]
        success = False
        for platform in platforms:
            try:
                modified_game = build_modified_game(open_id, access_token, platform)
                response_content = forward_majorlogin_request(modified_game)
                if response_content is not None:
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/octet-stream')
                    self.send_header('Content-Length', len(response_content))
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    self.wfile.write(response_content)
                    print(f"{GREEN}        ✅ We Are Modifying The request {RESET}")
                    success = True
                    break
            except Exception as e:
                print(f"{YELLOW}        Platform {platform} failed: {e}{RESET}")
                continue

        if not success:
            print(f"{RED}        All platforms failed. Forwarding original.{RESET}")
            try:
                resp = requests.post(MAJOR_LOGIN_URL, data=body, headers=dict(self.headers), verify=False, timeout=10)
                content = resp.content
                self.send_response(resp.status_code)
                self.send_header('Content-Type', 'application/octet-stream')
                self.send_header('Content-Length', len(content))
                self.send_header('Connection', 'close')
                self.end_headers()
                self.wfile.write(content)
            except Exception as e:
                print(f"{RED}        Error: {e}{RESET}")
                self.send_response(500)
                self.end_headers()

    def log_message(self, *args):
        pass

# ---------- Banner ----------
def print_banner():
    banner = f"""
{BOLD}{CYAN}
███╗   ███╗ █████╗ ███╗  ██╗██████╗ ███████╗██╗  ██╗
████╗ ████║██╔══██╗████╗ ██║██╔══██╗╚══███╔╝╚██╗██╔╝
██╔████╔██║███████║██╔██╗██║██║  ██║  ███╔╝  ╚███╔╝
██║╚██╔╝██║██╔══██║██║╚████║██║  ██║ ███╔╝   ██╔██╗
██║ ╚═╝ ██║██║  ██║██║ ╚███║██████╔╝███████╗██╔╝ ██╗
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚══╝╚═════╝ ╚══════╝╚═╝  ╚═╝
               {YELLOW}MANDZX PROXY{CYAN}
{RESET}
"""
    print(banner)

# ---------- Main ----------
if __name__ == '__main__':
    print_banner()
    
    # Ambil PORT dari environment Railway, fallback ke 5030
    port = int(os.environ.get("PORT", 5030))
    
    print(f"{BLUE}────────────────────────────────────────────────────────────────────{RESET}")
    print(f"{GREEN}        [*] Starting proxy server on port {port} ...{RESET}")
    
    server = HTTPServer(('0.0.0.0', port), DynamicHandler)
    server.handle_error = lambda *args: None
    
    print(f"{GREEN}        [✓] Server running. Press Ctrl+C to stop.{RESET}\n")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print(f"\n{YELLOW}        [!] Shutting down.{RESET}")
        server.shutdown()
        sys.exit(0)