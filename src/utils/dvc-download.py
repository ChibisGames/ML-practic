import hydra, subprocess
from omegaconf import DictConfig


@hydra.main(config_name="utils-config", config_path="../../configs", version_base="1.1")
def dvc_update(cfg: DictConfig) -> None:
    try:
        if cfg.PATH_TO_DVC.avoiding_duplication:
            subprocess.run(["dvc", "import-url", "--no-download", 
                            f"{cfg.PATH_TO_DVC.url}"], 
                            cwd=cfg.PATH_TO_DVC.target_dir, check=True)
        else:
            subprocess.run(["dvc", "import-url", 
                            f"{cfg.PATH_TO_DVC.url}"], 
                            cwd=cfg.PATH_TO_DVC.target_dir, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при DVC: {e}")

if __name__ == "__main__":
    dvc_update()
    