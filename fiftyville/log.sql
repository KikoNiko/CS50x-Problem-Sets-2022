-- Keep a log of any SQL queries you execute as you solve the mystery.
--July 28, 2021, Humphrey Street.
--Start by looking at crime_scene_reports for report about known day and location
SELECT description FROM crime_scene_reports
WHERE month = 7 AND day = 28 AND street = "Humphrey Street";

--the description gives us hints about time of theft (10:15am), mentions there were interviews with 3 witnesses and they point to the bakery.
--So next I will look into interviews table and check the transcripts for that day. I will also view the names of people interviewed.
SELECT transcript, name FROM interviews
WHERE month = 7 AND day = 28 AND year = 2021;
--I find that the 3 people interviewed are Ruth, Eugene and Raymond. They all talk about the theft and mention the bakery.
--Ruth says she saw the thief leave the parking lot within ten minutes of the theft (10:15-10:25am)
--Eugene tells us they saw the thief by Leggett Street ATM withdrawing money
--Raymond says the thief talked on the phone with someone for less than a minute talking about taking the earliest flight out of Fiftyville the next day.

--Having all this in mind lets first check bakery security logs
--I can also check the names and license plates of all people who exited the parking lot at that time
SELECT people.name, activity, people.license_plate
FROM bakery_security_logs
JOIN people ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
AND minute BETWEEN 15 AND 25
AND activity = "exit";
--p.s. I first had to see what are the types of activity and added the "exit" condition after

--Now we have a bunch of suspects so next lets check the ATM at Leggett Street
--Here again I can get people's names and account numbers by joining the two tables atm_transactions and bank accounts and then bank accounts with people.
SELECT people.name, bank_accounts.account_number
FROM atm_transactions
JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
JOIN people ON people.id = bank_accounts.person_id
WHERE year = 2021 AND month = 7 AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";
--p.s. I look at transaction_type withdraw to narrow even further. I added that condition later.
--The last two queries gave us a list of suspect names but some of them are matching.
--So we should try to get the names that are matching in both queries.
--I found the command 'intersect' to do that for me and now I narrowed down the suspects to 4 names (Bruce, Diana, Iman and Luca).
SELECT people.name
FROM bakery_security_logs
JOIN people ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2021 AND month = 7 AND day = 28 AND hour = 10
AND minute BETWEEN 15 AND 25
AND activity = "exit"
INTERSECT
SELECT people.name
FROM atm_transactions
JOIN bank_accounts ON atm_transactions.account_number = bank_accounts.account_number
JOIN people ON people.id = bank_accounts.person_id
WHERE year = 2021 AND month = 7 AND day = 28
AND atm_location = "Leggett Street"
AND transaction_type = "withdraw";


--Next lets look at phone calls
--We know they talked on the phone for less than a minute and their accomplice will buy a ticket
SELECT caller, receiver, duration FROM phone_calls
WHERE year = 2021 AND month = 7 AND day = 28
AND duration < 60;
--Here we see a bunch of phone numbers that we should link to the phone numbers of our thief and their accomplice
SELECT people.name, caller FROM phone_calls
JOIN people ON people.phone_number = phone_calls.caller
WHERE year = 2021 AND month = 7 AND day = 28 AND duration < 60;
--Now we see that from our 4 suspects only two pop up in this result.
--So I narrow down the suspects to 2 - Bruce and Diana.

--Next lets look at the flights. Would be helpful to know the Fiftyville airport id.
SELECT id FROM airports
WHERE city = "Fiftyville";
--Fiftyville airport id is 8
--Now lets find the flight
SELECT flights.id, airports.full_name, airports.city, flights.hour, flights.minute FROM flights
JOIN airports ON airports.id = flights.destination_airport_id
WHERE year = 2021 AND month = 7 AND day = 29
AND origin_airport_id = 8
ORDER BY hour;
--I see that the earliest flight is at 8:20 to NYC LaGuardia so that must be their flight.

--Now lets look at the passengers on that flight and see if our thief is there
SELECT people.name FROM people
JOIN passengers ON people.passport_number = passengers.passport_number
JOIN flights ON passengers.flight_id = flights.id
WHERE flights.id = 36;
--And now I see that there is a Bruce on this flight and no Diana so I can conclude Bruce is the thief!

--Now I must find the accomplice.
--To do that I will just track Bruce's call to see who he was calling.
SELECT phone_calls.id FROM phone_calls
JOIN people ON people.phone_number = phone_calls.caller
WHERE year = 2021 AND month = 7 AND day = 28
AND duration < 60
AND people.name = "Bruce";
--This gives me the call id (233) and now I can use it to find the receiver

SELECT people.name FROM people
JOIN phone_calls ON people.phone_number = phone_calls.receiver
WHERE year = 2021 AND month = 7 AND day = 28
AND duration < 60
AND phone_calls.id = 233;
--And now I see the name Robin comes up so Robin must be the accomplice!

