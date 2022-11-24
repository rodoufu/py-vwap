# py-vwap

It does not worry too much about logging or error handling, it's mostly just logging it with print.

To calculate the VWAP it's using 2 moving lists that can calculate their sum.
One for the numerator and another one for the denominator of the formula.

It is not using NumPy in order to focus on the code complexity and not on the specifics of the library.

For the moving list, it uses a circular list, so it does not need to allocate the memory every time an update happens.
And it caches the sum, this way it can update and calculate the sum in `O(1)`.
It hasn't covered some cases like an update with size 0 just for the sake of focusing on the solution and not treating the input.

It is using an async generator for getting the messages, in this case, it does not make that much of a difference but if it was publishing updates to a message broker and getting information from different sources it would help by not blocking on IO operations.
