import multiprocessing

workers = multiprocessing.cpu_count() * 2 + 1  # automático según CPU disponible
threads = 2  # cada worker puede atender 2 solicitudes simultáneas
timeout = 60  # suficiente para endpoints pesados como Prophet
capture_output = True  # logs visibles en Railway