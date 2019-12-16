import quantities as q
import water_interlock as w
import asyncio
import matplotlib.pyplot as plt
import time

async def update(port = "COM4", baudrate = 9600):
    tsensor = wl.TempSensorOld(q.TempUnit(q.TempUnit.Celsius), q.Temperature)
    fsensor = wl.FlowSensor(q.VoltUnit(q.VoltUnit.V), q.Voltage)
    w = wl.WaterInterlock(port, baudrate)
    w.setDataStructure(structure = ((16, tsensor), (8, fsensor)))
    return await W.check()
async def plot(data):
    t = time.time()
    T = [d for d in data]
    await plt.plot(T, data)
    plt.show()
async def close():
    