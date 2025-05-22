# Lichess

Initial commit



Considerations:
If SAN format is too slow, switch to bitboards. Currently using SAN because that's the format it comes in 



Todo:

Soon:
Think about if there's a way for similarity heuristic to return a move even if the next move in the similar position isn't legal

Before project MVP/release
Implement better data structures for faster lookups

After project MVP
Multithreading

At some point in the future, maybe never
Create your own chess bot feature, let users tune it themselves

Possible optimizations if needed:
Use bst instead of sorted tuple to calculate closest material value positions
Pass the material value of the current position to the next position so don't have to calculate every time