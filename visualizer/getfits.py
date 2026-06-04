from ftplib import FTP
import astropy.io.fits as FITS

def get_set(id):
    with FTP("data.asc-csa.gc.ca") as ftp:
        ftp.login()
        ftp.cwd("users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/2026/109/")

        with open(id, 'wb') as fp:
            ftp.retrbinary('RETR '+id, fp.write)

        ftp.quit()

def all_for_day(year:int, day:int):
    with FTP("data.asc-csa.gc.ca") as ftp:
        ftp.login()
        
        return get_all_for_day(ftp, year, day)

def get_all_for_day(ftp:FTP, year:int, day:int):
    ftp.cwd("users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/"+year.__str__()+"/"+day.__str__()+"/")
    return ftp.nlst()

def read_header_from_url(url): # ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/2026/109/NEOS_SCI_2026109004941_cord.fits.gz
    with FITS.open(url, use_fsspec=True) as hdul:
        with open(hdul[0].header['OBS_ID']+".txt", "w") as f:
            head = hdul[0].header.__str__()
            chnk = [ head[i:i+80] for i in range(0, len(head), 80) ]
            f.write("\n".join(chnk))
