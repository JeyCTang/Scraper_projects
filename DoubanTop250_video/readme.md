## Steps: 
1. check if the contents we want to collect are saved in the html page.
   1. if yes, we can collect the html source code directly [x]
   2. if no, then we have to find out where the contents are rendered

## Program process
1. Send the request to url
2. Get the html page content
3. Using regex to select required information
4. Save the data as json file