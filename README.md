# Ask_google

## Synopsis

Get answer from the google featuerd snippets.

## Installation
```bash
kalliope install --git-url https://github.com/corus87/ask_google
```
## Example
- Kalliope --> Ask google how tall is the eiffel tower
- Kalliope --> Ask google what time is it in Tokio
- Kalliope --> Ask google when albert einstein is born
- Kalliope --> Ask google how far is the moon from earth away

## Options
| parameter      | required | comments |
|----------------|----------|----------|
| question       | yes      |          |

## Output
| parameter          | return          |
|--------------------|-----------------|
| answer_found       | the answer      |
| answer_not_found   | the question    |

## Synpase
```
  - name: "ask-google"
    signals:
      - order: "ask google {{ question }}"
    neurons:
      - ask_google:
          question: "{{ question }}"
          file_template: "templates/google_answers.j2"  
```
## File template
```
{% if answer_found%} 
   On google I found: {{ answer_found }}
   
{% elif answer_not_found %} 
    I could not find an answer to {{ answer_not_found }}
    
{% endif %}
```

## Notes
This is an experimental neuron only! Because it does not exist a google API for instant answers, we scrap the google results from the featured snippets, so it is always possible that google will change the tags inside the html code again so the neuron will no longer work.
At this point we need to find the new tags provided for the different kind of snippets.
