import asyncio
import random
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device import Message

# Verbindungszeichenfolgen für die Geräte im Azure IoT Hub
CONNECTION_STRINGS = [
    "HostName=clcprojectbfr-iothub.azure-devices.net;DeviceId=raspberrystorage;SharedAccessKey=a3qx/epv21LdG09g7HamFcSFEjJ493Lgf8uKanV+gic=",
    "HostName=clcprojectbfr-iothub.azure-devices.net;DeviceId=raspberryoven;SharedAccessKey=pmhItOWzzlIVPLQJrHcW7o0/+B47Byt6zve2BfQT4O4=",
    "HostName=clcprojectbfr-iothub.azure-devices.net;DeviceId=raspberryfuegepress;SharedAccessKey=LZGIJzMcnRPKrx3xlZkm+kC6pKEpvAQ11/tPrWtkh+o=",
    "HostName=clcprojectbfr-iothub.azure-devices.net;DeviceId=raspberryrobot;SharedAccessKey=iXOgJaPwluTfYBeTh1doJsO/jEgjnDSl+9BYlYBwNl0=",
    "HostName=clcprojectbfr-iothub.azure-devices.net;DeviceId=raspberrywelder;SharedAccessKey=bC9n8zCg45PO7IczZ5tnTw7IfQMI3hqpj0OMOZ4AirQ="
]

# Produktionsschritte mit zugehörigen Wartezeiten und Simulationsfunktionen
PRODUCTION_STEPS = [
    {"name": "Roboterarm", "duration": 5, "simulate": lambda: {"action": "Werkstück aufgenommen"}},
    {"name": "Transport zu Schweißstation", "duration": 5, "simulate": lambda: {"distance": round(random.uniform(1.0, 5.0), 2)}},
    {"name": "Schweißen", "duration": 10, "simulate": lambda: {"welding_temperature": round(random.uniform(1200.0, 1500.0), 2)}},
    {"name": "Transport zu Ofen", "duration": 10, "simulate": lambda: {"distance": round(random.uniform(5.0, 10.0), 2)}},
    {"name": "Erwärmen im Ofen", "duration": 30, "simulate": lambda: {"oven_temperature": round(random.uniform(200.0, 250.0), 2), "time": 15}},
    {"name": "Fügen", "duration": 15, "simulate": lambda: {"fuegekraft": round(random.uniform(500.0, 1000.0), 2), "fuegeweg": round(random.uniform(0.1, 5.0), 2)}},
    {"name": "Kühlen", "duration": 10, "simulate": lambda: {"cooling_temperature": round(random.uniform(20.0, 25.0), 2)}},
    {"name": "Einlagerung", "duration": 5, "simulate": lambda: {"action": "In Speicher eingelagert"}}
]

# Funktion zur asynchronen Verbindung mit einem IoT Hub-Gerät
async def connect_device(connection_string):
    client = IoTHubDeviceClient.create_from_connection_string(connection_string)
    await client.connect()
    return client

# Asynchrone Funktion zur Simulation eines Produktionsschritts
async def simulate_step(step, in_queue, out_queue, client):
    while True:
        item = await in_queue.get()
        data = step["simulate"]()
        data["step"] = step["name"]
        data["item"] = item
        message = Message(str(data))
        await client.send_message(message)
        print(f"{step['name']} - Daten gesendet: {data}")
        await asyncio.sleep(step["duration"])
        if out_queue:
            await out_queue.put(item)
        in_queue.task_done()

# Hauptfunktion zur Simulation des Produktionsprozesses
async def main():
    # Verbindungen zu den Geräten herstellen
    clients = await asyncio.gather(*(connect_device(cs) for cs in CONNECTION_STRINGS))

    # Erstellen der Warteschlangen für die Produktionsschritte
    queues = [asyncio.Queue() for _ in PRODUCTION_STEPS]

    # Starten der Simulation für jeden Produktionsschritt
    tasks = []
    for i, step in enumerate(PRODUCTION_STEPS):
        in_queue = queues[i]
        out_queue = queues[i + 1] if i + 1 < len(PRODUCTION_STEPS) else None
        client = clients[i % len(clients)]
        task = asyncio.create_task(simulate_step(step, in_queue, out_queue, client))
        tasks.append(task)

    # Hinzufügen der Werkstücke zur ersten Station
    num_items = 1000  # Anzahl der zu verarbeitenden Werkstücke
    for item in range(1, num_items + 1):
        await queues[0].put(f"Werkstück {item}")
        await asyncio.sleep(5)  # Zeitverzögerung zwischen den Starts der Werkstücke

    # Warten, bis alle Queues leer sind
    await asyncio.gather(*(queue.join() for queue in queues))

    # Beenden der Simulation
    for task in tasks:
        task.cancel()
    await asyncio.gather(*tasks, return_exceptions=True)

    # Trennen der Verbindungen zu den Geräten
    for client in clients:
        await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
        out_queue = queues[i + 1] if i + 1 < len(PRODUCTION_STEPS) else None
        client = clients[i % len(clients)]
        task = asyncio.create_task(simulate_step(step, in_queue, out_queue, client))
        tasks.append(task)

    # Hinzufügen der Werkstücke zur ersten Station
    num_items = 1000  #         out_queue = queues[i + 1] if i + 1 < len(PRODUCTION_STEPS) else None
        client = clients[i % len(clients)]
        task = asyncio.create_task(simulate_step(step, in_queue, out_queue, client))
        tasks.append(task)

    # Hinzufügen der Werkstücke zur ersten Station
    num_items = 1000  #
        out_queue = queues[i + 1] if i + 1 < len(PRODUCTION_STEPS) else None
        client = clients[i % len(clients)]
        task = asyncio.create_task(simulate_step(step, in_queue, out_queue, client))
        tasks.append(task)

    # Hinzufügen der Werkstücke zur ersten Station
    num_items = 1000  #         out_queue = queues[i + 1] if i + 1 < len(PRODUCTION_STEPS) else None
        client = clients[i % len(clients)]
        task = asyncio.create_task(simulate_step(step, in_queue, out_queue, client))
        tasks.append(task)

    # Hinzufügen der Werkstücke zur ersten Station
    num_items = 1000  #
