import os
import requests
import time
import json


# 获取项目提交列表的函数
# 获取项目提交列表的函数
def get_commits(url, headers):
    """
    获取提交记录，支持分页和处理 GitHub API 的速率限制。
    :param url: 提交记录的请求 URL
    :param headers: 请求头
    :return: 提交记录的列表
    """
    commits = []
    while url:
        try:
            response = requests.get(url, headers=headers)

            # 处理速率限制
            if response.status_code == 429:
                print("Rate limit exceeded, waiting for reset...")

                reset_time = response.headers.get("X-RateLimit-Reset")

                if reset_time:
                    try:
                        reset_time = int(reset_time)
                        wait_time = reset_time - time.time()
                        if wait_time > 0:
                            print(f"Sleeping for {wait_time} seconds...")
                            time.sleep(wait_time + 5)
                        continue
                    except ValueError:
                        print("Error parsing X-RateLimit-Reset header. Retrying in 2 minutes...")
                        time.sleep(120)
                else:
                    print("No X-RateLimit-Reset header found. Retrying in 2 minutes...")
                    time.sleep(120)

            if response.status_code != 200:
                print(f"Failed to retrieve page: {url}")
                print(f"Status Code: {response.status_code}")
                print(f"Response Content: {response.content}")
                break

            commit_data = response.json()
            if not commit_data:
                print("No commits found!")
                break

            for commit in commit_data:
                commit_hash = commit['sha']
                commit_message = commit['commit']['message']
                commit_time = commit['commit']['committer']['date']
                commits.append({
                    "commit_hash": commit_hash,
                    "commit_message": commit_message,
                    "commit_time": commit_time
                })

            # GitHub API 分页
            if 'link' in response.headers:
                links = response.headers['link'].split(',')
                next_link = None
                for link in links:
                    if 'rel="next"' in link:
                        next_link = link.split(';')[0].strip('<>').strip()
                url = next_link
            else:
                url = None

        except requests.RequestException as e:
            print(f"Request error: {e}. Retrying in 2 minutes...")
            time.sleep(120)  # 等待2分钟再重新请求

    return commits


# 保存提交数据为 JSON 文件
def save_commits_to_file(commits, repo_name, file_path):
    """
    将提交记录保存为 JSON 格式文件。
    :param commits: 提交记录列表
    :param repo_name: 仓库名称，用于生成文件夹路径
    :param file_path: 文件路径，用于创建适当的文件夹结构
    """
    commit_dir =  file_path

    # 确保文件夹存在
    os.makedirs(commit_dir, exist_ok=True)

    output_file = os.path.join(commit_dir, "commits.json")
    with open(output_file, 'w') as file:
        json.dump(commits, file, indent=4)

    print(f"Commits have been saved to {output_file}")


# 保存 commit hash 到文本文件
def save_commit_hashes_to_file(commits, repo_name, file_path):
    """
    将提交的 hash 保存到单独的文本文件。
    :param commits: 提交记录列表
    :param repo_name: 仓库名称，用于生成文件夹路径
    :param file_path: 文件路径，用于生成适当的文件夹结构
    """
    commit_dir =  file_path

    # 确保文件夹存在
    os.makedirs(commit_dir, exist_ok=True)

    output_file = os.path.join(commit_dir, "patch_list.txt")
    with open(output_file, 'w') as file:
        for commit in commits:
            file.write(f"{commit['commit_hash']}\n")

    print(f"Commit hashes have been saved to {output_file}")



import json


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

    return repo_owner, repo_name, file_path, commit_sha,cve_id





# 主程序
def main():
    # 使用函数并读取 commit.json 中的信息
    json_file = 'commit.json'
    repo_owner, repo_name, file_path, commit_sha,cve_id = get_commit_info(json_file)
    print(f"Repo Owner: {repo_owner}")
    print(f"Repo Name: {repo_name}")
    print(f"File Path: {file_path}")
    print(f"Commit SHA: {commit_sha}")
    # URL 编码路径
    file_path_encoded = file_path.replace("/", "%2F")
    commits_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/commits?path={file_path_encoded}&sha={commit_sha}"
    print(f"Commits URL: {commits_url}")

    headers = {
        'Accept': 'application/vnd.github.v3+json',
    }
    # 动态生成输出文件名称
    file_path_parts = file_path.split('/')[-1].split('.')[0]
    print(file_path_parts)
    # 获取所有 commits
    commits = get_commits(commits_url, headers)

    # 如果有提交记录，保存到文件
    if commits:
        save_commits_to_file(commits, repo_name, cve_id)
        save_commit_hashes_to_file(commits, repo_name, cve_id)
    else:
        print("No commits found.")


if __name__ == "__main__":
    main()
