# Project: Theory Discourse Analysis
# Retrieve Crossref metadata for a theory-specific query and generate descriptive summaries and DOI lists

# Outputs (written to working directory):
# - Publisher_distribution.csv
# - Journals_distribution.csv
# - crossref_relevant_dois.csv
# Note: Requires internet access; uses Crossref API cursor-based paging.

###################################
#            CROSSREF             #
#            ARTICLES             #
###################################

##### Packages ####
library(rentrez)
library(fulltext)
library(xml2)
library(httr)
library(dplyr)
library(tidyr)
library(broom)
library(data.table)
library(jsonlite)

##### Retrieve metadata from Crossref ####

# Get request for Crossref using deep paging (no limits on size of query), get all DOIs and ISSN's for all available papers in PDF and XML format for search query "memory decay"
articles <- list()
# GET first 1000 article metadata, set cursor with first query
response <- GET(
  "https://api.crossref.org/works?query=memory%20decay&select=DOI,ISSN,publisher&cursor=*&rows=1000&filter=full-text.type:application/xml,full-text.type:application/pdf",
  timeout(20)
)

# Getting "response" in string format
# Parse response from string to named list
response <- content(response, "parsed") 
articles <- append(articles, response$message$items) 

# Repeat loop for fetching article metadata and binding it in object "articles"
i <- 0

repeat {
  query_string <- paste0(
    "https://api.crossref.org/works?query=memory%20decay&select=DOI,ISSN,publisher&rows=1000&filter=full-text.type:application/xml,full-text.type:application/pdf&cursor=",
    response$message[["next-cursor"]]
  )
  print(query_string)
  response <- GET(query_string, timeout(20))
  response <- content(response, "parsed")
  if (length(response$message$items) == 0) break
  articles <- append(articles, response$message$items)
  i <- i + 1
  Sys.sleep(0.1)  # optional but nice
}

##### Create publisher distribution table ####

# Create key value pairs for publisher distribution
publishers <- list()
publishers[["NA"]] <- 0
subject_count <- 0

# Loop for filling publishers list
for (article in articles) {
  if (is.null(article$publisher)) {
    publishers[["NA"]] <- publishers[["NA"]] + 1
    next
  }
  if (is.null(publishers[[article$publisher]])) {
    publishers[[article$publisher]] <- 1
  } else {
    publishers[[article$publisher]] <- publishers[[article$publisher]] + 1
  }
}

# Sort list in ascending order
publisher_distribution <- publishers[order(-unlist(publishers))]

# Create data frame for csv table
publisher_distribution <- data.frame(publishers=names(publisher_distribution),
                                     count=unname(unlist(publisher_distribution))) 

write.csv(publisher_distribution, "Publisher_distribution.csv", row.names = F)


##### Create journal distribution table ####

# Create key value pairs for journal-title distribution -> same procedure as for the publishers, only the ISSN's must be translated into journal names additionally
issn_list <- list()
issn_list[["NA"]] <- 0
journal_count <- 0

# Fill list with ISSN's from articles
for (article in articles) {
  issn <- NA
if (!is.null(article$ISSN) && length(article$ISSN) >= 1) {
  issn <- article$ISSN[[1]]
}
if (is.na(issn)) {
  issn_list[["NA"]] <- issn_list[["NA"]] + 1
  next
}

  if (is.null(issn_list[[issn]])) {
    issn_list[[issn]] <- 1 
  } else {
    issn_list[[issn]] <- issn_list[[issn]] + 1 
  }
}

# Create key value pairs
journal_list <- list()
journal_list[["NA"]] <- issn_list[[1]]

# Set counter to two since first position is NA
i <- 2

# Fill list with journal names and count of articles
for (issn in names(issn_list)[2:length(issn_list)]) { 
  print(issn)
  query_string <- paste0("https://api.crossref.org/journals/", issn)
  response <- GET(query_string, timeout(20))

  if (response$status_code == 404) { 
    print("Journal not found")
    journal_list[["NA"]] <- journal_list[["NA"]] + 1 
    next
  }
  response <- content(response) 
  journal_name <- response$message$title 
  journal_list[[journal_name]] <- issn_list[[i]] 
  i <- i + 1
}

# Sort list in ascending order
journals_distribution <- journal_list[order(-unlist(journal_list))]

# Create data frame for csv table
journals_distribution <- data.frame(Journal=names(journals_distribution),
                                    Count=unname(unlist(journals_distribution))) 

write.csv(journals_distribution, "Journals_distribution.csv", row.names = F)

issn_list_sorted <- issn_list[order(-unlist(issn_list))]

relevant_issn <- c("0090-502x", "1750-6980", "0028-0836", "1069-9384", 
                   "0006-4971", "1747-0218", "0956-7976", "0340-0727", 
                   "1943-3921", "0033-3131")
relevant_articles <- Filter(function(x) {
  !is.null(x$ISSN) && length(x$ISSN) >= 1 && tolower(x$ISSN[[1]]) %in% relevant_issn
}, articles)
relevant_dois <- vapply(relevant_articles, function(x) if (!is.null(x$DOI)) x$DOI else NA_character_, character(1))
relevant_dois <- relevant_dois[!is.na(relevant_dois)]
write.table(relevant_dois, "crossref_relevant_dois.csv", sep = ",", col.names = FALSE, row.names = FALSE, quote = FALSE)

