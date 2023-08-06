[![pipeline status](https://gitlab.com/PaniR/rero/badges/master/pipeline.svg)](https://gitlab.com/PaniR/rero/commits/master)
[![coverage report](https://gitlab.com/PaniR/rero/badges/master/coverage.svg)](https://gitlab.com/PaniR/rero/commits/master)
[![PyPI version](https://badge.fury.io/py/rero.svg)](https://badge.fury.io/py/rero)

*Rero* is an efficient communication protocol intended for transmissions of byte frames over e.g. a serial interface or buses.
It builds upon [COBS](https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing) which allows for a minimum encoding overhead.
It is perfectly suited for MCUs with DMA support.

Did somebody asked what is it good for? Here are some qualities of Rero:

| Quality     | How                          | Good for                             |
|-------------|------------------------------|--------------------------------------|
| Reliable    | CRC check                    | Checking integrity of frame          |
| Robust      | [COBS](https://en.wikipedia.org/wiki/Consistent_Overhead_Byte_Stuffing) and [COBSR](https://github.com/cmcqueen/cobs-c) byte stuffing           | Easy to resynchronize byte stream    |
| Efficient   | Exploit properties of COBS and COBSR   | Minimum processing overhead          |
| Scalable    | Customize Rero to your needs | Minimize frame overhead              |
| Bus-capable | Optional address field       | Address frame for specific recipient |

A C implementation written for STM32 MCUs is available [here](https://gitlab.com/PaniR/rero_stm32). It builds upon a very efficient ring buffer implementation tailored for UART interfaces, which of course utilizes DMA support for transmission and reception.

## Quick start

Rero requires Python 3.5 or newer to run.

```bash
$ pip install rero
```

## Usage

```python
import rero

reroPacker = rero.Packer(1) 	# own address = 1

# Dummy payload
payload = bytes([1, 2, 3, 4])

msgToSend = reroPacker.pack(payload, 20) # Packing with dedicated address = 20

# msgToSend may now be sent e.g. by use of pySerial...

# Unpack received frame
for payloadRcd in reroPacker.unpack(msgToSend):
	print(payloadRcd)
```
	
Further examples are given in the [docs](https://panir.gitlab.io/rero).

## Documentation

You can find the documentation at [here](https://panir.gitlab.io/rero).

## Contribution
For information on how to contribute to the project, please check the [Contributor's Guide](CONTRIBUTING.md).

## Contact
Please use the [Gitlab service desk](incoming+panir-rero-11417024-issue-@incoming.gitlab.com) or if you have a Gitlab account you may directly open an [issue](https://gitlab.com/PaniR/rero/issues).

## License
[MIT License](LICENSE)