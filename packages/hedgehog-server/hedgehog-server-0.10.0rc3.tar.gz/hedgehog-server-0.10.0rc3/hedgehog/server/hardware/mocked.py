from typing import Any, Dict, Generic, List, Set, Tuple, TypeVar

import trio
import bisect

from . import HardwareAdapter, HardwareUpdate, POWER


T = TypeVar('T')


class MockedState(Generic[T]):
    def __init__(self) -> None:
        self._times: List[float] = []
        self._values: List[T] = []

    def set(self, time: float, value: T) -> None:
        i = bisect.bisect_left(self._times, time)
        if i < len(self._times) and self._times[i] == time:
            self._values[i] = value
        else:
            self._times.insert(i, time)
            self._values.insert(i, value)

    def get(self, time: float=None, default: T=None)-> T:
        if time is None:
            time = trio.current_time()

        i = bisect.bisect_right(self._times, time)
        if i == 0:
            return default
        return self._values[i - 1]


class MockedUpdates:
    def __init__(self) -> None:
        self._updates: Dict[float, Set[HardwareUpdate]] = {}

    def add(self, time: float, update: HardwareUpdate) -> None:
        try:
            updates = self._updates[time]
        except KeyError:
            updates = self._updates[time] = set()
        updates.add(update)

    async def __aiter__(self):
        while self._updates:
            next_time = min(self._updates)
            await trio.sleep_until(next_time)
            updates = self._updates.pop(next_time)
            for update in updates:
                yield update


class MockedHardwareAdapter(HardwareAdapter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.io_configs: Dict[int, int] = {}
        self.emergency: bool = False
        self._updates: MockedUpdates = MockedUpdates()
        self._imu_rate: MockedState[Tuple[int, int, int]] = MockedState()
        self._imu_acceleration: MockedState[Tuple[int, int, int]] = MockedState()
        self._imu_pose: MockedState[Tuple[int, int, int]] = MockedState()
        self._analogs: List[MockedState[int]] = [MockedState() for port in range(16)]
        self._digitals: List[MockedState[bool]] = [MockedState() for port in range(16)]
        self._motors: List[MockedState[Tuple[float, float]]] = [MockedState() for port in range(4)]

    async def __aenter__(self):
        await super().__aenter__()
        nursery = await self._stack.enter_async_context(trio.open_nursery())

        @nursery.start_soon
        async def emit_updates():
            async for update in self._updates:
                self._enqueue_update(update)

    async def get_version(self):
        return bytes(12), 3, 0

    async def emergency_action(self, activate):
        self.emergency = activate

    async def get_emergency_state(self) -> bool:
        return self.emergency

    async def set_io_config(self, port, flags):
        self.io_configs[port] = flags

    def set_analog(self, port: int, time: float, value: int) -> None:
        self._analogs[port].set(time, value)

    async def get_analog(self, port):
        return self._analogs[port].get(default=0)

    def set_imu_rate(self, time: float, x: int, y: int, z: int) -> None:
        self._imu_rate.set(time, (x, y, z))

    async def get_imu_rate(self):
        return self._imu_rate.get(default=(0, 0, 0))

    def set_imu_acceleration(self, time: float, x: int, y: int, z: int) -> None:
        self._imu_acceleration.set(time, (x, y, z))

    async def get_imu_acceleration(self):
        return self._imu_acceleration.get(default=(0, 0, 0))

    def set_imu_pose(self, time: float, x: int, y: int, z: int) -> None:
        self._imu_pose.set(time, (x, y, z))

    async def get_imu_pose(self):
        return self._imu_pose.get(default=(0, 0, 0))

    def set_digital(self, port: int, time: float, value: bool) -> None:
        self._digitals[port].set(time, value)

    async def get_digital(self, port):
        return self._digitals[port].get(default=False)

    async def set_motor(self, port, mode, amount=0, reached_state=POWER, relative=None, absolute=None):
        # TODO set_motor
        pass

    def set_motor_state(self, port: int, time: float, velocity: int, position: int) -> None:
        self._motors[port].set(time, (velocity, position))

    async def get_motor(self, port):
        return self._motors[port].get(default=(0, 0))

    async def set_motor_position(self, port, position):
        # TODO set_motor_position
        pass

    async def set_motor_config(self, port, config):
        # TODO set_motor_config
        pass

    async def set_servo(self, port, active, position):
        # TODO set_servo
        pass

    async def send_uart(self, data):
        # TODO send_uart
        pass

    async def set_speaker(self, frequency):
        # TODO set_speaker
        pass
