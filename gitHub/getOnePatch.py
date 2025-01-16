import os
import json
def extract_file_patch(diff_file_path, target_file_path):
    """
    从指定的 diff 文件中提取特定文件的补丁
    """
    patch_lines = []
    inside_patch = False

    with open(diff_file_path, 'r', encoding='utf-8') as f:
        diff_lines = f.readlines()

    for line in diff_lines:
        # 找到目标文件的 diff 开始标志
        if line.startswith(f"diff --git a/{target_file_path}"):
            inside_patch = True  # 开始提取目标文件的补丁内容

        if inside_patch and line.startswith("diff --git a/") and not line.startswith(f"diff --git a/{target_file_path}"):
            inside_patch = False  # 停止提取目标文件的补丁
        # 如果正在提取目标文件的补丁，收集补丁行
        if inside_patch:
            patch_lines.append(line)

        # 如果遇到下一个文件的 diff 开始标志，停止提取


    return patch_lines if patch_lines else None


def process_commit_files(commits_dir,save_dir, target_file_path):
    """
    从下载的 commit 文件中提取特定文件的补丁
    """
    # 创建一个存储补丁的文件夹
    patch_dir = f"{save_dir}/change_low_version"
    if not os.path.exists(patch_dir):
        os.makedirs(patch_dir)

    # 遍历 commit 文件
    for commit_file in os.listdir(commits_dir):
        commit_file_path = os.path.join(commits_dir, commit_file)

        # 只处理 .diff 文件
        if commit_file.endswith('.txt'):
            print(f"Processing {commit_file_path}...")

            # 提取目标文件的补丁
            patch = extract_file_patch(commit_file_path, target_file_path)

            if patch:
                # 使用目标文件名作为补丁文件的名字
                # target_file_name = os.path.basename(target_file_path)
                patch_file_name = f"{commit_file}"
                patch_file_path = os.path.join(patch_dir, patch_file_name)

                with open(patch_file_path, 'w', encoding='utf-8') as patch_file:
                    patch_file.writelines(patch)

                print(f"Patch saved: {patch_file_path}")
            else:
                print(f"No patch found for {target_file_path} in {commit_file_path}")

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

def main():
    repo_owner, repo_name, file_path, commit_sha,cve_id= get_commit_info('./commit.json')
    file_path_parts = file_path.split('/')[-1].split('.')[0]
    commits_dir = f'{cve_id}/patches'  # 本地保存 commit .diff 文件的目录
    target_file_path = file_path  # 你想要提取的目标文件名称

    # 处理本地的 commit 文件并提取目标文件的补丁
    process_commit_files(commits_dir,cve_id, target_file_path)


if __name__ == "__main__":
    main()
