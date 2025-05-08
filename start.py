import sys
import multiprocessing
import os
from run import runweb

def worker(port):
	server = runweb.AppServerManager()
	server.start(port = port)

if __name__ == '__main__':
	jobs = []
	ports = [int(os.getenv('PORT'))]

	for port in ports:
		p = multiprocessing.Process(target=worker, args=(port,))
		jobs.append(p)
		p.start()