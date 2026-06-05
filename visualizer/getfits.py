from ftplib import FTP
import astropy.io.fits as FITS
from visualizer.models import ObservationSet
import time

def get_set(id):
    with FTP("data.asc-csa.gc.ca") as ftp:
        ftp.login()
        ftp.cwd("users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/2026/109/")

        with open(id, 'wb') as fp:
            ftp.retrbinary('RETR '+id, fp.write)

        ftp.quit()

def all_for_day(year:int, day:int):
    all = []
    with FTP("data.asc-csa.gc.ca") as ftp:
        ftp.login()
        
        all = day_list(ftp, year, day)
        #no_type = [elem[:-8] for elem in all]
        ftp.close()
    raw = []
    cor = []
    cord = []
    for elem in all:
        if "_cord" in elem:
            cord.append(elem)
        elif "_cor" in elem:
            cor.append(elem)
        else:
            raw.append(elem)
    
    pausetime = 10
    baseurl = "ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/"+year.__str__()+"/"+day.__str__()+"/"
    no_dupes = []

    for elem in raw:
        has_cor = False
        has_cord = False
        for cor_elem in cor:
            if elem[:-8] in cor_elem:
                has_cor = True
                cor.remove(cor_elem)
                break
        for cord_elem in cord:
            if elem[:-8] in cord_elem:
                has_cord = True
                cord.remove(cord_elem)
                break

        no_dupes.append("|".join([elem, True.__str__(), has_cor.__str__(), has_cord.__str__()]))
        
        # save_header(baseurl+elem, year, day, True, has_cor, has_cord)

        # print("Imported: "+elem)
        # time.sleep(pausetime)
    
    for elem in cor:
        has_cord = False
        for cord_elem in cord:
            if elem[:-8] in cord_elem:
                has_cord = True
                cord.remove(cord_elem)
                break
        
        no_dupes.append("|".join([elem, False.__str__(), True.__str__(), has_cord.__str__()]))
    
    for elem in cord:
        no_dupes.append("|".join([elem, False.__str__(), False.__str__(), True.__str__()]))
    
    summary_str = "\n".join(no_dupes)

    with open(year.__str__()+"-"+day.__str__()+".txt", "w") as file:
       file.write(summary_str)
    
    get_remaining(year, day)

def get_remaining(year:int, day:int):
    lines = []
    pausetime = 10
    with open(year.__str__()+"-"+day.__str__()+".txt", "r") as file:
       lines = file.readlines()

    while len(lines) > 0:
        line = (lines.pop()).split("|")

        save_header("ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/"+year.__str__()+"/"+day.__str__()+"/"+line[0],
                    year, day, 'True' in line[1], 'True' in line[2], 'True' in line[3])
        # print("users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/"+year.__str__()+"/"+day.__str__()+"/"+line[0],
        #             year, day, 'True' in line[1], 'True' in line[2], 'True' in line[3])
        time.sleep(pausetime)
        
        with open(year.__str__()+"-"+day.__str__()+".txt", "w") as file:
            file.write("".join(lines))
    


def day_list(ftp:FTP, year:int, day:int):
    ftp.cwd("users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/"+year.__str__()+"/"+day.__str__()+"/")
    return ftp.nlst()

# def read_header(url): # ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/2026/109/NEOS_SCI_2026109004941_cord.fits.gz
#     with FITS.open(url, use_fsspec=True, memmap=False) as hdul:
#         with open(hdul[0].header['OBS_ID']+".txt", "w") as f:
#             head = hdul[0].header.__str__()
#             chnk = [ head[i:i+80] for i in range(0, len(head), 80) ]
#             f.write("\n".join(chnk))

def save_header(url, year:int, day:int, has_raw:bool, has_cor:bool, has_cord:bool): # ftp://data.asc-csa.gc.ca/users/OpenData_DonneesOuvertes/pub/NEOSSAT/ASTRO/2026/109/NEOS_SCI_2026109004941_cord.fits.gz
    with FITS.open(url, use_fsspec=True, memmap=False, cache=False) as hdul:
        obs = create_observation(hdul[0].header, year, day, has_raw, has_cor, has_cord, False)
        obs.save()
        del obs
        hdul.close()
        del hdul

def create_observation(header, year:int, day:int, has_raw:bool=True, has_cor:bool=False, has_cord:bool=False, has_clean:bool=False):
    return ObservationSet(
        xbinning = header['XBINNING'],
        ybinning = header['YBINNING'],
        creator = header['CREATOR'],
        telescop = header['TELESCOP'],
        exposure = header['EXPOSURE'],
        aexptime = header['AEXPTIME'],
        rexptime = header['REXPTIME'],
        date_obs = header['DATE-OBS'],
        time_obs = header['TIME-OBS'],
        cmdra = header['CMDRA'],
        cmddec = header['CMDDEC'],
        cmdrol = header['CMDROL'],
        cmdq0 = header['CMDQ0'],
        cmdq1 = header['CMDQ1'],
        cmdq2 = header['CMDQ2'],
        cmdq3 = header['CMDQ3'],
        ra = header['RA'],
        dec = header['DEC'],
        objctra = header['OBJCTRA'],
        objctdec = header['OBJCTDEC'],
        objctrol = header['OBJCTROL'],
        ela_min = header['ELA_MIN'],
        ela_max = header['ELA_MAX'],
        ela_ang = header['ELA_ANG'],
        sun_min = header['SUN_MIN'],
        sun_max = header['SUN_MAX'],
        temp_ccd = header['TEMP_CCD'],
        object = header['OBJECT'],
        observer = header['OBSERVER'],
        intent = header['INTENT'],
        instrume = header['INSTRUME'],
        targtype = header['TARGTYPE'],
        prop_id = header['PROP_ID'],
        title = header['TITLE'],
        moving = header['MOVING'],
        geo_lat = header['GEO_LAT'],
        geo_long = header['GEO_LONG'],
        imgstate = header['IMGSTATE'],
        archive = header['ARCHIVE'],
        obs_type = header['OBSTYPE'],
        obs_id = header['OBS_ID'],
        year = year,
        day = day,
        raw = has_raw,
        cor = has_cor,
        cord = has_cord,
        clean = has_clean
    )