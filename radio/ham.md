# Amateur Radio Technician License Study Notes

## Exam Overview

- 35 multiple-choice questions
- Passing score: 26 correct
- Current question pool: 2026–2030
- Main goal: understand concepts and memorize ham-specific rules

---

## 1. Commission's Rules
- Control operator AND station licensee responsible for proper operation of station
- Wait to transmit until license is **ON THE DATABASE** (grace period is for renewing it only)
- 219-220 MHz for **Fixed digital message forwarding only**
  - Data usually reserved for lowest part of the band
  - Specifically, non-data allowed in 222-225 MHz
  - No exceeding 50 W PEP
- Can communicate with countries who have not notified ITU (international telecomm union) that it objects
- Transmitting phone signals need to send call sign with phone or morse
- Frequency Coordinator: "An entity, **recognized in a local or regional area by amateur operators whose stations are eligible to be auxiliary or repeater stations**, that recommends transmit/receive channels and associated operating and technical parameters for such stations in order to avoid or minimize potential interference."
- Never transmit without control operator
- Yield to non-Amateurs on restricted bands
  - 
- Technician or higher for ISS comms
- Can operate on US vessel with master's permission for international waters
- Compensation for operation only if part of classroom
- Only 10 meter band phone privileges for Technician (HF)
- Club must have at least 4 members
- 3rd party: someone to another person on BEHALF of a third person
- Callsigns
  - 1-2 letters, 1 digit, 3 letters
- Anyone can be operator of satellite if allowed to transmit
- Any station can be remotely controlled
- Auxiliary station:
  - Supports another station's operations by relay or control link
- Encoding ONLY for spacecraft
- Stroke/slash/slant for separators
- Technician, General, Amateur Extra
- Remote control: operating a station over internet
- International comms are permitted on behalf of Amateur radio service and self
- SSB can be used in at least some segment in all bands above 50 MHz
- Start of band is for CW only (50-50.1 and 144-144.1)
- 10 years for FCC amateur license

## 2. Operating Procedures
- CQ: calling any station
- Repeater offset: diff between RX/TX freq
  - 2m VHF: 600 KHz
  - 70cm UHF: 5 MHz
  - 1.25m: 1.6MHz
- Call station on repeater
  - Their sign then my sign
- Band plan: for amateur band in region (FCC decides spectrum though)
- 146.520 MHz - National Simplex Calling Frequency (from ARRL 2 meter band plan)
- [Q codes](https://www.qsl.net/w5www/qcode.html)
  - QSY: change frequency
- Simplex channels
  - In UHF/VHF band plan, like a repeater but same frequency
- DTMF: dual tone, multi frequency (signaling to repeater)
- Continuous Tone-Coded Squelch System: sub-audible (67-250 Hz) tone to gate squelch
- FM dropping out could be peaking from voice
- Net practice: only transmit when directed
- RACES (radio amateur civil emergency service)
  - emergency management and civil defense comms
  - need to have civil defense certification
- CQ response: other call sign then yours
- Winlink is email over ham radio
  - CALL@winlink.com
- Can transmit outside frequency privileges for human or property concern
- VHF/UHF transceiver "reverse" function to swap TX and RX frequencies
- Digital color code on DMR (Digital Mobile Radio) repeater is access code a transmitter can use to access specific receiver

## 3. Radio Wave Propagataion
- Tropospheric ducting: differential temperature layer in atmosphere
- 10m and 6m NOT affected by water/rain much
- Electric field direction determines polarization
- VHF/UHF antennas with opposite polarization can't pick up entire field, so reduced received signal strength
- high HF signals refracted to Earth during high sunspot F region
  - 10m (28 MHz) and 6m (50 Mhz) around there
  - Higher frequencies pass through.
- Horizontal polarization for long distance CW and SSB on VHF and UHF
- Long distance on 10 meter band requires ionization
- Sporadic E (10,6,2m bands)
- Picket fencingL flutter on mobile signals (multipath propagation)

## 4. Amateur Radio Practices
- Short, heavy gauge wire to minimize voltage drop
- Excessive gain on SSB gives distorted transmitted audio
  - (Exceeds circuitry range)
- FT8 weak-signal digital mode
  - Capable of low S/N 
  - Transceiver connected to input and output of computer
- Electronic keyer: manual sending of morse code

## 5. Electrical Principles
- 3dB = factor of 2

## 6. Electronics and Electrical Components

## 7. Practical Circuits
- PTT: Push to talk, where it switches from receive to transmit
- "Over-deviating" for modulating in frequency too much (spilling out the sides) so talk quieter (in FM specifically)
- Net Control Station (NCS): "traffic cop" of a net
  - Orderly comm, logs, discipline
- Net could be social or emergency
- Ultraviolet light could damage the jacket and cause water to enter
- Solid state transmitters reduce power for high SWR so reflected power doesn't hurt transistors
- Check TV coaxial connectors if getting TV interference
- Antenna analyzer for determining resonance
- No acid-core solder
- Foam-dielectric coax (compared to solid-dielectric coax)
  - Less loss per foot
  - More damaged by moisture
- Switch to select SSB or CW-FM on VHF
  - changes amp for proper operation
  - SSB mode - delay to keep amp keyed between voice peaks to prevent chatter (like between speaking, it turning on and off)
  - CW-FM - instant switching 
- Transverter: RF input and output of transceiver to another band
- Mixer: convert signal from one freq to another
- Directional wattmeter for SWR

## 8. Signals and Emissions
- ARQ: Automatic Repeat reQuest
  - If receiving station detects error, it asks sender to repeat
- Satellites transmit health and status
- [Grid locator](http://www.arrl.org/grid-squares) (grid square): lat/lon location shorthand
- Amateur radio mesh network
  - many-to-many WiFi self-routing network
- AM fast-scan TV transmission: 6 MHz
- Linear transponder sats:
  - Transmit continuous beacon
  - If uplink power too low, downlink won't register very well, so compare to beacon
- VoIP: Voice Over Internet
- Contesting: operators try to contact as many stations as possible during a period. get points
- FM: VHF packet radio transmission
- Only 1 signal for FM received at a time compared to SSB
- EchoLink (for internet comms): must register call sign and proof of license
- NTSC (national TV systems committee): analog fast-scan color TV
- SSB has narrower bandwidth
- How is over the air access to Internet Radio Linking Project (IRLP) nodes accomplished?
  -  Dual-Tone Multi-Frequency (DTMF) signals


- SSB (single side-band): 
- AM
- PM
- DRM

## 9. Antennas and Feed Lines
- Antenna loading
  - Inserting inductors to lengthen to resonate to desired freq
- RG
  - RG-213: Heavy duty 50-Ohm, larger conductor, less loss than RG-58
- Lowest loss for NO dielectric (perfect insulator)
- Loose connection in antenna or feed link causes erratic SWR changes

## 0. Safety
- Fast discharging of battery causes overheating/out-gassing
- Station licensee responsible for FCC exposure limits (50W PEP for VHF, 200W for other)
- Avoid sharp bends
- Humans abosorb VHF (30M Hz to 300 MHz) so MPE (max exposure limits) are most restrictive
- Local electric codes for requirements of amateur radio tower or antenna
- 10 feet of power wires or more
- Radio is NON-ionizing









### License Classes

- Technician
- General
- Amateur Extra

### Frequency Privileges

| Band | Technician Privileges | Notes |
|---|---|---|
| 2 meters |  |  |
| 70 centimeters |  |  |
| 10 meters |  |  |
| 6 meters |  |  |

### Important Rules

- Station identification:
- Control operator:
- Control point:
- Third-party communications:
- Prohibited transmissions:
- Emergency communications:
- Music and broadcasting:
- Business communications:

### Facts to Memorize

- 
- 
- 

---

## 2. Operating Procedures

### Making a Contact

1. Listen before transmitting.
2. Confirm the frequency is clear.
3. Say:
   - `CQ CQ CQ`
   - Your call sign
4. Identify at required intervals.

### Repeaters

- Repeater:
- Input frequency:
- Output frequency:
- Offset:
- CTCSS tone:
- Simplex:
- Duplex:

### Common Terms

| Term | Meaning |
|---|---|
| CQ | Calling any station |
| QSO | Radio contact |
| QTH | Location |
| QRZ | Who is calling me? |
| QRM | Human-made interference |
| QRN | Natural interference |
| RST | Readability, strength, tone |

### Phonetic Alphabet

| Letter | Word | Letter | Word |
|---|---|---|---|
| A | Alfa | N | November |
| B | Bravo | O | Oscar |
| C | Charlie | P | Papa |
| D | Delta | Q | Quebec |
| E | Echo | R | Romeo |
| F | Foxtrot | S | Sierra |
| G | Golf | T | Tango |
| H | Hotel | U | Uniform |
| I | India | V | Victor |
| J | Juliett | W | Whiskey |
| K | Kilo | X | X-ray |
| L | Lima | Y | Yankee |
| M | Mike | Z | Zulu |

---

## 3. Radio-Wave Propagation

### Core Relationships

\[
c = f\lambda
\]

Where:

- \(c\): speed of light
- \(f\): frequency
- \(\lambda\): wavelength

Approximate antenna wavelength formula:

\[
\lambda\text{ in meters} \approx \frac{300}{f\text{ in MHz}}
\]

### Propagation Types

#### Line of Sight

- Common on:
- Limited by:
- Radio horizon compared with visual horizon:

#### Ionospheric Propagation

- Common on:
- Affected by:
- Day versus night behavior:

#### Other Effects

- Multipath:
- Fading:
- Tropospheric ducting:
- Sporadic E:
- Meteor scatter:
- Knife-edge diffraction:

### Polarization

- Horizontal:
- Vertical:
- Circular:
- Polarization mismatch causes:

---

## 4. Radio Operation and Station Setup

### Radio Controls

| Control | Purpose |
|---|---|
| Squelch |  |
| RF gain |  |
| AF gain |  |
| RIT |  |
| Filter width |  |
| Scan |  |
| Memory |  |

### Basic Station Signal Path

```text
Power Supply
    |
Transceiver
    |
SWR Meter
    |
Feed Line
    |
Antenna
```

### Mobile Installation

- Power connection:
- Fuse placement:
- Grounding:
- Antenna placement:
- Avoiding vehicle interference:

---

## 6. Electronic Components

### Passive Components

#### Resistor

- Function:
- Unit:
- Common uses:

#### Capacitor

- Function:
- Behavior with DC:
- Behavior with AC:
- Common uses:

#### Inductor

- Function:
- Behavior with changing current:
- Common uses:

### Semiconductor Components

#### Diode

- Allows current:
- Common uses:
- Polarity markings:

#### LED

- Function:
- Requires:

#### Transistor

- Function:
- Types:
- Common uses:

#### FET

- Controlled primarily by:
- Common uses:

### Other Components

- Transformer:
- Relay:
- Voltage regulator:
- Integrated circuit:
- Fuse:
- Switch:

### Schematic Symbols

- [ ] Resistor
- [ ] Capacitor
- [ ] Inductor
- [ ] Diode
- [ ] LED
- [ ] Transistor
- [ ] Ground
- [ ] Battery
- [ ] Transformer
- [ ] Switch

---

## 7. Radio Circuits and Troubleshooting

### Receiver Blocks

```text
Antenna
  |
RF Amplifier
  |
Mixer
  |
Intermediate Frequency
  |
Detector
  |
Audio Amplifier
  |
Speaker
```

### Transmitter Blocks

```text
Microphone
  |
Audio Processing
  |
Modulator
  |
Oscillator
  |
RF Amplifier
  |
Antenna
```

### Important Definitions

- Sensitivity:
- Selectivity:
- Oscillator:
- Mixer:
- Modulator:
- Demodulator:
- Amplifier:

### Common Problems

| Symptom | Possible Cause |
|---|---|
| High SWR |  |
| Weak received signal |  |
| Distorted transmitted audio |  |
| RF feedback |  |
| Receiver overload |  |
| No output power |  |
| Intermittent signal |  |

### Test Equipment

- Multimeter:
- SWR meter:
- Wattmeter:
- Dummy load:
- Oscilloscope:
- Antenna analyzer:

---

## 8. Signals and Emissions

### Modulation Types

| Mode | Meaning | Typical Use |
|---|---|---|
| AM | Amplitude modulation |  |
| FM | Frequency modulation |  |
| SSB | Single sideband |  |
| CW | Continuous wave |  |
| Digital | Digitally encoded signal |  |

### Bandwidth

- FM bandwidth:
- SSB bandwidth:
- CW bandwidth:
- Digital mode bandwidth:

### Digital Modes

- APRS:
- Packet radio:
- DMR:
- FT8:
- EchoLink:
- Error correction:

### Amateur Satellites

- Uplink:
- Downlink:
- Beacon:
- Transponder:
- Doppler shift:
- Tracking software:
- Satellite operating etiquette:

---

## 9. Antennas and Feed Lines

### Antenna Types

#### Dipole

- Radiation pattern:
- Polarization:
- Approximate length:

#### Vertical

- Radiation pattern:
- Polarization:
- Ground-plane requirements:

#### Directional Antenna

- Examples:
- Gain:
- Front-to-back ratio:
- Beamwidth:

### Half-Wave Dipole Length

\[
L_{\text{feet}} \approx \frac{468}{f_{\text{MHz}}}
\]

Each side is approximately:

\[
L_{\text{side}} \approx \frac{234}{f_{\text{MHz}}}
\]

### Feed Lines

| Type | Advantages | Disadvantages |
|---|---|---|
| Coaxial cable |  |  |
| Ladder line |  |  |

### SWR

- Standing-wave ratio measures:
- Ideal SWR:
- High SWR indicates:
- Possible consequences:
- Antenna tuner function:

### Connectors

- PL-259:
- SO-239:
- BNC:
- N-type:
- SMA:

---

## 10. Safety

### Electrical Safety

- Turn off power before:
- Capacitors may:
- Fuse placement:
- Grounding:
- Battery short-circuit hazards:

### Antenna Safety

- Minimum distance from power lines:
- Proper mast installation:
- Fall protection:
- Weather considerations:

### Lightning Safety

- Disconnect:
- Ground:
- Lightning arrestor:
- Do not operate during:

### RF Exposure

RF exposure depends on:

- Frequency
- Transmitter power
- Antenna gain
- Distance
- Duty cycle
- Transmission mode

Definitions:

- Controlled environment:
- Uncontrolled environment:
- Duty cycle:
- RF exposure evaluation:

---

# Equations Cheat Sheet

\[
V = IR
\]

\[
P = VI
\]

\[
P = I^2R
\]

\[
P = \frac{V^2}{R}
\]

\[
\lambda = \frac{c}{f}
\]

\[
\lambda_{\text{m}} \approx \frac{300}{f_{\text{MHz}}}
\]

\[
L_{\text{dipole, ft}} \approx \frac{468}{f_{\text{MHz}}}
\]

---

# Memorization List

## FCC Rules

- [ ] Identification interval
- [ ] Technician frequency privileges
- [ ] Maximum permitted power
- [ ] Prohibited communications
- [ ] Emergency exceptions
- [ ] Control operator responsibilities

## Operating

- [ ] Standard repeater offsets
- [ ] Common Q signals
- [ ] Phonetic alphabet
- [ ] Calling procedures
- [ ] Emergency net procedures

## Technical

- [ ] Ohm’s law
- [ ] Power equations
- [ ] Metric prefixes
- [ ] Component symbols
- [ ] Antenna formulas
- [ ] SWR meaning

## Safety

- [ ] Power-line clearance
- [ ] Lightning procedures
- [ ] RF exposure factors
- [ ] Fuse placement
- [ ] Battery safety

<!-- ---

# Missed Practice Questions

## Question 1

**Question:**

**My answer:**

**Correct answer:**

**Why I missed it:**

**Rule or concept to remember:**

---

## Question 2

**Question:**

**My answer:**

**Correct answer:**

**Why I missed it:**

**Rule or concept to remember:**

---

# Final Review

- [ ] Complete one pass through every category
- [ ] Memorize frequency privileges
- [ ] Review all missed questions
- [ ] Score at least 85% on several practice exams
- [ ] Review safety and FCC rules immediately before the exam -->