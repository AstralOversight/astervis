# Astervis
Welcome to Astervis, a browser-based FITS database and visualizer.

## Setting up Astervis (Locally)
Prerequisites:
1. Visual Studios Code (Run the Dev Container)
2. WSL (Windows Subsystem for Linux) (Optional but reccomended)
3. Access to this Git repository

Steps:
1. Using Git, clone this repository to your desired location (in WSL if present)
2. Rename the `.env-blank` file to `.env` and complete the missing lines
    - Add a `DJANGO_SECRET_KEY`
    - Add Django superuser credentials if desired
    - Clear the `DJANGO_BASE_URL` (since we are running this locally)
3. Open the repository as a Dev Container in VS Code
4. Wait for the container to build and run
5. Head to http://localhost/ to verify functioning of site

Adding observations:
1. Set up a Django admin/superuser account
    - This can either be done automatically using the environment variables or manually via `python manage.py createsuperuser`
2. Log in using those credentials at https://localhost/admin/
3. Click the button to add an observation location
    - The Domain should be something like `data.asc-csa.gc.ca` and the "S path" would be like `/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/2026`
4. Wait a bit (depends on how many folders/sub-folders exist)
5. Return to the main site and view all the observations
