import os
import json
import random
import subprocess
import requests
from datetime import datetime

# ==== الإعدادات الحساسة ====
OPENAI_API_KEY = "sk-proj-..."  # ← اختصرته هنا
GITHUB_TOKEN = "github_pat_..."  # ← اختصرته هنا
SSH_KEY_PUBLIC = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIN9EGJGHRk//Ut5srxzKY+3kOTBtj3OW6+ztXSpMmXWc mbomadian23@gmail.com"
SSH_KEY_PRIVATE_PATH = "/data/data/com.termux/files/home/.ssh/id_ed25519"
NETLIFY_HOOK_URL = "https://api.netlify.com/build_hooks/68869d063815467dc63e38c8"
GIT_REPO = "git@github.com:public36/zuku.git"
SITE_DIR = "dist" if os.path.exists("dist") else "."

# ==== توليد مفتاح SSH إن لم يكن موجودًا ====
def generate_ssh_key():
    if os.path.exists(SSH_KEY_PRIVATE_PATH):
        return

    print("🔧 Generating new SSH key...")

    email = "mbomadian23@gmail.com"
    ssh_dir = os.path.dirname(SSH_KEY_PRIVATE_PATH)
    os.makedirs(ssh_dir, exist_ok=True)

    subprocess.run([
        "ssh-keygen", "-t", "ed25519", "-C", email,
        "-f", SSH_KEY_PRIVATE_PATH, "-N", ""
    ], check=True)

    os.chmod(SSH_KEY_PRIVATE_PATH, 0o600)
    os.chmod(SSH_KEY_PRIVATE_PATH + ".pub", 0o644)

    subprocess.run(["eval", "$(ssh-agent -s)"], shell=True)
    subprocess.run(["ssh-add", SSH_KEY_PRIVATE_PATH], check=True)

    # إضافة مفتاحك اليدوي (المُعطى)
    with open(SSH_KEY_PRIVATE_PATH + ".pub", "a") as pubkey_file:
        pubkey_file.write("\n" + SSH_KEY_PUBLIC + "\n")

    print("✅ SSH key generated and updated.")

# ==== تحديث المنتجات ====
def update_products():
    file_path = "products.json"
    products = []

    if os.path.exists(file_path):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                products = json.load(f)
        except json.JSONDecodeError:
            print("⚠️ Invalid JSON file. Creating a new list.")
            products = []

    new_product = {
        "id": len(products) + 1,
        "name": f"AI Product {random.randint(1000, 9999)}",
        "image": f"https://picsum.photos/300?random={random.randint(1, 9999)}",
        "description": "Generated automatically by AI.",
        "price": f"{random.randint(10, 100)} €"
    }

    products.append(new_product)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(products, f, indent=2, ensure_ascii=False)

    print(f"🆕 Product added: {new_product['name']}")

# ==== GitHub Push ====
def push_to_github():
    if not os.path.exists(".git"):
        print("❌ Current directory is not a Git repository.")
        return

    print("📤 Pushing changes to GitHub...")
    os.environ["GIT_SSH_COMMAND"] = f"ssh -i {SSH_KEY_PRIVATE_PATH}"

    subprocess.run(["git", "add", "."], check=True)
    subprocess.run(["git", "config", "user.email", "mbomadian23@gmail.com"])
    subprocess.run(["git", "config", "user.name", "Auto Bot"])

    result = subprocess.run(
        ["git", "commit", "-m", f"Auto update {datetime.now().isoformat()}"],
        capture_output=True,
        text=True
    )

    if "nothing to commit" in result.stdout.lower():
        print("📭 Nothing to commit.")
        return

    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ Changes pushed to GitHub.")

# ==== Netlify Deploy ====
def trigger_netlify():
    print("🌐 Triggering Netlify build...")
    try:
        res = requests.post(NETLIFY_HOOK_URL)
        if res.status_code == 200:
            print("✅ Netlify build triggered.")
        else:
            print(f"⚠️ Netlify trigger failed: {res.status_code}")
    except Exception as e:
        print(f"❌ Netlify error: {e}")

# ==== Main ====
def main():
    print("\n🚀 Starting full update and deployment...\n")

    generate_ssh_key()

    if not os.path.exists(SSH_KEY_PRIVATE_PATH):
        print(f"❌ SSH key not found at: {SSH_KEY_PRIVATE_PATH}")
        return

    update_products()
    push_to_github()
    trigger_netlify()

    print("\n✅ All tasks completed.")

if __name__ == "__main__":
    main()