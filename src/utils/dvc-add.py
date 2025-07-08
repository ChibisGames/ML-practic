# Добавление файла(ов) в DVC
import hydra, subprocess
from omegaconf import DictConfig


@hydra.main(config_name="utils-config", config_path="../../configs", version_base="1.1")
def dvc_add(cfg: DictConfig) -> None:
    try:
        if cfg.method_of_application == "local":
            target_dir = cfg.PATH_TO_DVC.target_dir
            internal_files = [target_dir + '/' + i for i in \
                              cfg.PATH_TO_DVC.internal_files]
            # Добавление внутренних файлов
            for file in internal_files:
                subprocess.run(["dvc", "add", 
                                f"{file}"], check=True)

        elif cfg.method_of_application == "gdrive": # Способ не работает с 01.01.2025
            # Добавление файла в DVC
            subprocess.run(["dvc", "add", 
                            f"{cfg.PATH_DVC_TO_GDRIVE.repo_path}/{cfg.PATH_DVC_TO_GDRIVE.repo_name}"], check=True)

            # Фиксация изменений в Git
            subprocess.run(["git", "add", 
                            f"{cfg.PATH_DVC_TO_GDRIVE.repo_path}/{cfg.PATH_DVC_TO_GDRIVE.repo_name}.dvc", 
                            ".gitignore"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}")


def git_commit():
    try:
        subprocess.run(["git", "commit", "-m", 
                        f"Track commit with DVC"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при коммите: {e}")

if __name__ == "__main__":
    dvc_add()
    # git_commit()