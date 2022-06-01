from multiprocessing.pool import Pool
import signal
import traceback
from types import GeneratorType
from pickle import PicklingError
import dill

def init_worker(function):
    def worker_function(arguments):
        signal.signal(signal.SIGINT, signal.SIG_IGN)
        results = function(**arguments)
        if isinstance(results,GeneratorType):
            results = [item for item in results]
        return results
    return dill.dumps(worker_function)

def run_function(payload):
    function, arguments = payload
    worker_function = dill.loads(init_worker(function))
    return worker_function(arguments)

def multiprocess(function,arguments,pool_size):
    pool_size =  max(1,min(10,pool_size))
    payload = []
    for arg in arguments:
        payload.append((function,arg))
    try:
        with Pool(processes=pool_size) as pooled_tasks:
            results = pooled_tasks.imap_unordered(run_function,payload)
            pooled_tasks.close()
            pooled_tasks.join()
            returns = []
            for result in results:
                if isinstance(result,list):
                    returns += result
                else:
                    returns.append(result)
        return returns
    except Exception as e:
        function_name = function.__name__
        line_number = "?"
        for line in traceback.format_exc().split("\n"):
            if function_name in line:
                line_number = line.split(", ")[1].replace("line ","")
        if not e.args:
            e.args = ("",)
        e.args = [f"Child process executing function \"{function_name}\" encountered an error on line {line_number}. {e.args[0]}"]+[arg for arg in range(1,len(e.args))]
        raise e from None
