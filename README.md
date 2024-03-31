# Popcap .SAF Extractor/Packer
Extracts or packs Popcap's proprietary .SAF files

Usage: `safExtractor.py <.saf file> <output path>`

Note: Packer is W.I.P, The checksum is quite difficult to reverse engineer. The final packer will consist of getting an example game to generate the checksums for us first, and then building the file.

The games that I'm aware of that use .SAF are:
```
Feeding Frenzy 2 Deluxe
Feeding Frenzy Deluxe
Iggle Pop Deluxe
Pizza Frenzy
Talismania Deluxe
Word Harmony Deluxe
```

## SAF File structure
A SAF file is composed of the following structure:  
`0x00000000`: 4 Byte Magic number (46 46 41 53 01)  
`0x00000008`: 4 Byte `FILE_LIST_BEGIN` location  
This points to the beginning of the file list structure, starting with a whole file checksum  
`0x00000008` - 0xFILE_LIST_START-1: Sequential raw binary file data 
### File List (0xFILE_LIST_BEGIN)
`0xFILE_LIST_BEGIN`: 20 Byte checksum of the entire file (minus the checksum itself) 

For readability, `0xFILE_LIST_ITEM` = `0xFILE_LIST_BEGIN+20`  
`0xFILE_LIST_ITEM`: 4 Byte offset for the starting location of the binary file data.  
`0xFILE_LIST_ITEM+4`: 4 Byte length of file  
`0xFILE_LIST_ITEM+8`: 16 Byte Checksum of file  
`0xFILE_LIST_ITEM+24`: 1 Byte length of file path  
`0xFILE_LIST_ITEM+26`: <file path length> byte file path string  
`0xFILE_LIST_ITEM+26`: Empty Byte

Next file begins at `0xFILE_LIST_ITEM+26+<file path length>`
![SAF Diagram](https://i.imgur.com/tg0hQSg.png)
