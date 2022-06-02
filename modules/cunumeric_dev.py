import modules.conda
import modules.cuda as cuda
import modules.jupyter

def cunumeric_env(writer, cudaVersionShort):
    short = float(cudaVersionShort)
    repo = "mfoerste4"
    branch = "branch-22.07"
    writer.emit("""RUN wget "https://raw.githubusercontent.com/$repo/cunumeric/$branch/conda/environment-test-3.9.yml" \\
        -O /tmp/cunumeric_dev.yaml""",
                repo=repo,
                branch=branch)
    writer.condaEnv("/tmp/cunumeric_dev.yaml", "cunumeric_dev", deleteYaml=True)
    #writer.condaPackages(["ccache", "clang=11.0.0", "clang-tools=11.0.0"],
    #                     channels=["conda-forge"], cmd="mamba")


def emit(writer, **kwargs):
    modules.conda.emit(writer)
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    _, _, cudaVersionShort, _ = cuda.shortVersion(kwargs["cudaVersion"])
    cunumeric_env(writer, cudaVersionShort)
    modules.jupyter.emit(writer, **kwargs)
    writer.emit("COPY contexts/envs/cunumeric-dev /cunumeric-dev")
