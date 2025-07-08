# Чтение данных в Google Drive через DVC 
# (По идее работает, по факту google блокирует из-за защиты конфиденциальности)
import hydra, subprocess
from omegaconf import DictConfig


@hydra.main(config_name="utils-config", config_path="../../configs", version_base="1.1")
def dvc_pull(cfg: DictConfig) -> None:
    try:
        subprocess.run(["dvc", "pull", 
                        f"{cfg.PATH_DVC_TO_GDRIVE.repo_path}/{cfg.PATH_DVC_TO_GDRIVE.repo_name}",
                        "-r", cfg.PATH_DVC_TO_GDRIVE.remote_name], check=True)
        print("Данные скачаны из Google Drive!")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка: {e}")


if __name__ == "__main__":
    dvc_pull()