from __future__ import absolute_import
import modules.dev_env
import modules.cuda
import modules.internal
import modules.cunumeric_dev
import modules.openmpi


def emit(writer, **kwargs):
    if "cudaVersion" not in kwargs:
        raise Exception("'cudaVersion' is mandatory!")
    if "base" not in kwargs:
        raise Exception("'base' is mandatory!")
    if "rcUrl" not in kwargs:
        kwargs["rcUrl"] = None
    modules.cuda_dev.emit(writer, kwargs["cudaVersion"], kwargs["base"],
                          kwargs["rcUrl"])
    modules.cunumeric_dev.emit(writer, **kwargs)
    modules.openmpi.emit(writer)
    modules.dev_env.emit(writer, **kwargs)

    writer.emit("ENV TERM=xterm-256color")

def images():
    imgs = {}
    for osVer in ["20.04"]:
        verStr = osVer.replace(".", "")
        for cudaVer in ["11.4", "11.5"]:
            _, _, cu_short, _ = modules.cuda.shortVersion(cudaVer)
            cu_short = cu_short.replace(".", "")
            imgName = "cunumeric-dev:%s-%s" % (verStr, cu_short)
            imgs[imgName] = {
                "cudaVersion": cudaVer,
                "base": "ubuntu:%s" % osVer,
                "needsContext": True,
            }
    imgs.update(modules.internal.read_rc())
    return imgs
