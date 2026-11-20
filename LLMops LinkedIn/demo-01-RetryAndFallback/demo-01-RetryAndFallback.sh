########## Building Retry and Fallback Logic for Production LLM Applications ##########

############################################################
# 1. Foundry Project Setup — Credentials and Model Deployment
# 2. Launch Jupyter Notebook
# 3. Install resilience libraries
# 4. Imports, client setup, and model names
# 5. Prove the real deployment works
# 6. Break it: raw crash, no handling
# 7. Add retry only
# 8. Add fallback on top
# 9. Put it together: one reusable function
############################################################


#######################################
# 1. Foundry Project Setup — Credentials and Model Deployment
#######################################

# Start in the Microsoft Foundry portal

# Build -> Models - these following models should already be deployed

gpt-5.4-nano # this will be our primary deployment
gpt-4.1-nano # this will be our fallback deployment


#######################################
# 2. Launch Jupyter Notebook
#######################################

# Set up the launch of the notebook behind the scenes
# Make sure you export the Open AI key in the terminal (behind the scenes)
# Just start with the named notebook open

# Remaining please look at jupyternotebook : RetryAndFallback.ipynb







