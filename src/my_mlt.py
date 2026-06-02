from dataclasses import dataclass
from melt import Melt


app = Melt()


@app.command()
def hello(msg: str):
    """say hello base on given name"""
    print("hello", msg)


@app.switch()
def output(path: str):
    """write a output file with some content for test"""
    with open(path, "w") as file:
        file.write("switch is working .....")


@app.switch()
def ouit(name: str): # -ou -> outut
    """i write this now"""
    print("fuuck you", name)


@app.switch()
def ouiq(name: str): 
    print("fuckkkkkkkkkkkkkk", name)


@dataclass
class IOStream:
    input: str = ""
    output: str = ""


if __name__ == "__main__":
    app()
