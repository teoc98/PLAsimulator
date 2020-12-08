# PLAsimulator

[![License: GPL](https://img.shields.io/badge/license-GPLv3-red)](https://github.com/teoc98/PLAsimulator/blob/main/LICENSE)

**PLAsimulator** is a [Programmable Logic Array](https://en.wikipedia.org/wiki/Programmable_logic_array) simulator written in Python 2.7/3.

<!-- GETTING STARTED -->
## Getting Started
### Prerequisites
* [NumPy](http://numpy.scipy.org/)
* [tkinter](https://docs.python.org/3/library/tkinter.html)

Necessary to rebuild the documentation: 
* [Epydoc](http://epydoc.sourceforge.net/)

### Installation
Just clone the repo
   ```sh
   git clone https://github.com/teoc98/PLAsimulator.git
   ```

<!-- USAGE EXAMPLES -->
## Usage

### Command line usage
```sh
python pla.py [-x x_size][-i n_inputs][-o n_outputs][-a n_and] 
```

Options:
* ```-h, --help```: show help message and exit
* ```-x <x_size>```: window width in pixels
* ```-i <n_inputs>```: number of input pins
* ```-o <n_outputs>```: number of output pins (equal to the number of OR gates)
* ```-a <n_and>```: number of AND gates

_For more examples, please refer to the [Documentation](https://example.com)_

### Circuits library
The built-in circuits library contains by default the following circuits: 
* 1 bit half adder
* 1 bit full adder
* 2 bit adder
* 6-bit ones' complement
* 4-bit twos' complement
* 2 bit multiplicator
* 6 bit square root floor
* reductor 3-2
* multiple logic gate
* priority encoder
* multiplexer
* majority
* decoder
* decoder 4 bit - 7 segment
* shift register
* comparator
* one step flip-flop SR
* one step flip-flop T
* one step flip-flop JK
* Parity check (CRC-1)
* CRC-3-GSM

Where the CRC code generator polynomial are:
* CRC-1: ![formula](https://render.githubusercontent.com/render/math?math=x%2B1)
* CRC-3-GSM: ![formula](https://render.githubusercontent.com/render/math?math=x^3%2Bx%2B1)

### Circuits development
It is possible to extend the circuits library by creating new ```Circuit``` objects, using standard NumPy matrix notation. 

To create a new circuit from a boolean function it is possible to use the following functions: 
```python
generate_code(name, description, function, input_names, output_names)
generate_obj(description, function, input_names, output_names)
```
Function ```generate_code``` prints the code to paste into the module, while function ```generate_obj``` returns a new ```Circuit``` object. 

Parameters:
* ```function``` must be a function that accepts as input a boolean ```n_i```-tuple and returns a boolean ```n_o```-tuple; 
* ```input_names``` must be a tuple of ```n_i``` strings; 
* ```output_names``` must be a tuple of ```n_o``` strings. 

Please note that in order to add a circuit to the simulator circuit library, is necessary to add it to list ```circs``` in module ```circuits.py```. 

## Notes
Unfortunately most of the user guide and documentation is in Italian only.  
* Project webpage: [https://matteo.ga/pla/](https://matteo.ga/pla/)
* First version webpage by Alice Plebe: [https://www.dmi.unict.it/scollo/slidy/share/simulators/PLA_simulator_1_0/index-en.html](https://www.dmi.unict.it/scollo/slidy/share/simulators/PLA_simulator_1_0/index-en.html)

<!-- LICENSE -->
## License
Distributed under the GNU General Public License (GNU GPL) version 3. See `LICENSE` for more information.
