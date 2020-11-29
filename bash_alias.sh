alias gbc='for line in $(git branch); do 
     description=$(git config branch.$line.description)
     if [ -n "$description" ]; then
       echo "$line     $description"
     else
       echo "$line"
     fi
done'
