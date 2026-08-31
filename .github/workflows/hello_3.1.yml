name: Hello World 

on: 
    push:
      branches: 
       - main
      paths-ignore:
        - '**/*.md'
    schedule:
      - cron: '30 4 * * *'    
    workflow_dispatch:
        inputs:
         your_name:
             description : "Enter your name"
             required: true
             default: 'Avanish'
             type: string
         gretting:
             description: "Select your welcome msg"
             required: true
             default: 'Hi' 
             type: choice
             options:
               - 'Hi'
               - 'hello'
               - 'Ram Ram'
               
env:    
  TZ: 'Asia/Kolkata'

jobs: 
    MyJobs:
        runs-on: ubuntu-latest

        steps:
            - name: Echo Name 
              run: |
               echo "Selected Greeting: ${{ github.event.inputs.gretting }}"
               echo "Entered Name: ${{ github.event.inputs.your_name }}"

            - name: Echo Time 
              run: echo "Current time in IST $(date)" 

            - name: Print Triggered Event
              run: |
                  echo "The event that triggered this workflow is: ${{ github.event_name }}"
