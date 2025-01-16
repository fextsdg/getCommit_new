import requests
import os
import json
import time  # 导入 time 模块来实现等待


def get_commit_info(json_file):
    # 打开并读取 commit.json 文件
    with open(json_file, 'r') as f:
        commit_data = json.load(f)

    # 提取所需的字段
    repo_owner = commit_data.get("repo_owner")
    repo_name = commit_data.get("repo_name")
    file_path = commit_data.get("file_path")
    commit_sha = commit_data.get("commit_sha")
    cve_id = commit_data.get("CVE_ID")

    return repo_owner, repo_name, file_path, commit_sha, cve_id


# GitHub仓库的基本信息
GITHUB_API_URL = "https://api.github.com/repos/{owner}/{repo}/commits"
OWNER, REPO, FILE_PATH, _ ,cve_id= get_commit_info("commit.json")
file_path_parts = FILE_PATH.split('/')[-1].split('.')[0]

# 提供一组commit SHA，你可以从文件中读取或直接在代码中指定
with open(fr'{cve_id}\patch_list.txt', 'r') as f:
    COMMITS_SHA_LIST = [line.strip() for line in f.readlines()]


def get_patch(commit_sha, owner, repo):
    """
    获取指定commit的patch，处理访问频繁错误
    """
    url = f"https://github.com/{owner}/{repo}/commit/{commit_sha}.diff"

    while True:  # 进入循环，直到请求成功或达到预期的重试条件
        try:
            response = requests.get(url)

            if response.status_code == 200:
                return response.text
            else:  # 处理其他错误
                print(f"Error fetching patch for commit {commit_sha}: {response.status_code}. Retrying in 5 minutes...")
                if response.status_code == 429:
                    print(f"Too many requests. Retrying in 5 minutes... (HTTP 429)")
                time.sleep(300)  # 等待 5 分钟后重试
        except requests.exceptions.RequestException as e:
            print(f"Request failed with error: {e}. Retrying in 5 minutes...")
            time.sleep(300)  # 等待 5 分钟后重试


def download_patches(commits_sha, owner, repo):
    """
    根据commit号下载补丁文件
    """
    file_dir = os.path.join(cve_id, "patches")
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    i = 1
    for commit_sha in commits_sha:
        patch = get_patch(commit_sha, owner, repo)
        if patch:
            file_name = f"{i}_{commit_sha}.txt"
            file_path = os.path.join(file_dir, file_name)
            with open(file_path, "w", encoding='utf-8') as f:
                f.write(patch)
            print(f"Patch saved: {file_path}")
            i+=1


def main():
    # 使用给定的commit SHA下载补丁
    download_patches(COMMITS_SHA_LIST, OWNER, REPO)


if __name__ == "__main__":
    main()
