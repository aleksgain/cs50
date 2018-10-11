# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

Lung disease caused by inhaling fine ash or dust.. Also, seems to be a made-up word?..

## According to its man page, what does `getrusage` do?

Returns the resource usage for the calling process, its children or thread.

## Per that same man page, how many members are in a variable of type `struct rusage`?

16

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

Not sure but I'd guess to save resources by avoiding unnecessary copying.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

The for loop goes throught the file one word at a time until it reaches end of file (EOF). It achieves this by iterating
through the words one char at a time and making sure that only alphabetical chars (isalpha) and apostrophes ('\'') are allowed. Then it
checks against the defined max word length and words with numbers and shifts iterating index to 0 if either condition is met to discard
and get ready for new word. Once the word is found (i.e. isalpha or '\'', !EOF), it sends the word to check function declared in dictionary.c
file and checks resource usage before and after the return value to calculate the time spent on resolving the correctness of the word.
Check returns a boolean so if fasle, incorrect word is recored and incorrect word counter is updated.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

Effieiency, easier to discard the word early on and jump to the next one if an incorrect char is found.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

From what I understand, for safety and efficiency. The loaded parameters cannot be changed which means that the code is faster to compile
and less prone to errors due to accidental changes..
