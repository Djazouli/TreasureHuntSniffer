This is a very simple sniffer, just to get use to protocol sniffing.
The idea is to run the sniffer while doing a treasure hunt on the MMORPG D0fus.
Of course, it has been done for educational purposes only, and shouldn't be used in game. 

It works pretty simply, you just need to create a protocol.pk file, by decompiling the swf source code, and parsing it smartly.
Everything is explained on the [LaBot GitHub page](https://github.com/louisabraham/LaBot), and all the needed code is here.
By the way, all the protocol decoding inside the labot folder comes from here (commit 1150067).

To run it, just run 
```bash
python main.py
```

Then, start a treasure hunt. The sniffer should automatically catch the next hint you have to find, and display something like.
```bash
You have to aim towards [-3, -22]
```

Then, go to this map, and validate the hint. The path to the next hint will then appear in the console.

```bash
You have to aim towards [-3, -22]
Next hint is a phorreur, I'll tell you when we get there.
```

If the hint in a Phorreur, just walk in the right direction, and the sniffer will detect when you encounter the phorreur.

```bash
You have to aim towards [-3, -22]
Next hint is a phorreur, I'll tell you when we get there.
Found phorreur in [-3, -20]
```

Then proceed to the end of the hunt, and the output will look like
```bash
You have to aim towards [-3, -22]
Next hint is a phorreur, I'll tell you when we get there.
Found phorreur in [-3, -20]
You have to aim towards [-10, -20]
You have to aim towards [-14, -20]
You have to aim towards [-20, -20]
You have to aim towards [-20, -10]
You have to aim towards [-21, -10]
You have to aim towards [-21, -8]
Next hint is a phorreur, I'll tell you when we get there.
Found phorreur in [-23, -8]
You have to aim towards [-23, -10]
You have to aim towards [-25, -10]
Fighting time!
Took 278.7446451187134 seconds
```

Then you're ready to launch another hunt !