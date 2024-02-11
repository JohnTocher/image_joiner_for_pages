# image_joiner_for_pages
Utility for stitching images with some overlap - created for scans or renders of ebook facing pages

I had an ebook purchased in epub format, which didn't render correctly.  
It was image heavy and was splitting the single page into two not quite even pages.  
I tried using Calibre (an amazing tool generally) but couldn't get it to convert the ePub to a pdf correctly. It's possible that it is my own incompetence here, but I couldn't solev it.  
Instead I ran the eBook viewer and took screenshots of each page, and then wrote this utility to crop the relevant parts of each page and then combine them into a single page image.  
The utility then combines the images into a single PDF file.

The three steps are relatively separted in the code, so if you only need a part of them, it should be easy enough to do, simply comment out the parts of process_all_files() that you don't require.
