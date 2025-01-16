import requests
import os
repo_owner = "libtiff"
repo_name = "libtiff"
project_url = f"{repo_owner}/{repo_name}"  # 项目名称
FILE_PATH = "libtiff/tif_lzw.c"  # 替换为文件的路径
# GitLab仓库的基本信息
GITLAB_API_URL = "https://gitlab.com/api/v4/projects/{project_id}/repository/commits"

file_path_parts = FILE_PATH.split('/')[-1].split('.')[0]
def get_project_id(project_url):
    gitlab_api_url = "https://gitlab.com/api/v4/projects/"
    project_url_encoded = project_url.replace("/", "%2F")

    response = requests.get(gitlab_api_url + project_url_encoded)
    if response.status_code == 200:
        project_info = response.json()
        return project_info['id']
    else:
        print(f"Failed to fetch project info: {response.status_code}")
        print(f"Error Details: {response.text}")
        return None

# 提供一组commit SHA，你可以从文件中读取或直接在代码中指定
with open(fr'{repo_name}\{file_path_parts}\commits.txt', 'r') as f:
    COMMITS_SHA_LIST = [line.strip() for line in f.readlines()]

PROJECT_ID = get_project_id(project_url)

def get_patch(commit_sha, project_id):
    """
    获取指定commit的统一diff补丁
    """
    url = f"https://gitlab.com/api/v4/projects/{project_id}/repository/commits/{commit_sha}/diff"
    print(url)
    return
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # 返回的就是一个JSON数组，包含了diff信息
    else:
        print(f"Error fetching patch for commit {commit_sha}: {response.status_code}")
        return None

def download_patches(commits_sha, project_id):
    """
    根据commit号下载统一diff补丁
    """
    file_dir = os.path.join(repo_name, file_path_parts, "patches")
    if not os.path.exists(file_dir):
        os.mkdir(file_dir)
    for commit_sha in commits_sha:
        patch = get_patch(commit_sha, project_id)
        if patch:
            # 拼接文件路径，保存为统一diff补丁
            file_name = f"{file_path_parts}-{commit_sha}.c"
            file_path = os.path.join(file_dir, file_name)
            with open(file_path, "w", encoding='utf-8') as f:
                # 将diff格式数据保存
                for diff in patch:
                    f.write(diff['diff'] + "\n")
            print(f"Patch saved: {file_path}")

def main():
    # 使用给定的commit SHA下载补丁
    download_patches(COMMITS_SHA_LIST, PROJECT_ID)

if __name__ == "__main__":
    main()
