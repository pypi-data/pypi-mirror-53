''' API for PRYSM

Feng Zhu (fengzhu@usc.edu)
2018-12-15 16:12:22
'''
from . import icecore
from . import tree
from . import coral
from . import lake
from . import speleo
import numpy as np
import os
import itertools
import LMRt
import xarray as xr
import random
from scipy.stats.mstats import mquantiles
#  from IPython import embed



def forward(psm_name, lat_obs, lon_obs,
            lat_model, lon_model, time_model,
            prior_vars, elev_obs=None, elev_model=None,
            latlon_search_mode=None,
            latlon_ind_dict=None, record_id=None,
            verbose=False, **psm_params):

    ''' Forward environmental variables to proxy variables

    This is a major wrapper of the PSMs.
    It assumes that VS-Lite has been installed in R via:
        ```R
        install.packages("devtools")
        devtools::install_github("fzhu2e/VSLiteR")
        ```

    Args:
        psm_name (str): options are `coral_d18O`, `ice_d18O`, `tree_trw`
        lat_obs, lon_obs (float): the location of the proxy site
        lat_model, lon_model (1-D/2-D array): the grid points of the model simulation
        prior_vars (dict): the dictionary that stores the prior variables in Pandas DataArray, including
            - tas (3-D array): surface air temperature in (time, lat, lon) [K]
            - pr (3-D array): precipitation rate in (time, lat, lon) [kg/m2/s]
            - psl (3-D array): sea-level pressure in (time, lat, lon) [Pa]
            - d18O (3-D array): precipitation d18O in (time, lat, lon) [permil]
            - d18Ocoral (3-D array): coral d18O in (time, lat, lon) [permil]
            - d18Osw (3-D array): seawater d18O in (time, lat, lon) [permil]
            - tos (3-D array): sea-surface temperature in (time, lat, lon) [K]
            - sos (3-D array): sea-surface salinity in (time, lat, lon) [permil]
        psm_params (kwargs): the specific parameters for certain PSMs

    Returns:
        pseudo_value (1-D array): pseudoproxy timeseries
        pseudo_time (1-D array): the time axis of the pseudoproxy timeseries

    '''
    def run_psm_for_coral_d18O():
        sst = np.array(prior_vars_dict['sst']) - 273.15  # convert to degC
        sst_sub = np.array(sst[:, lat_ind, lon_ind])
        if np.all(np.isnan(sst_sub)):
            print(f'PRYSM >>> sst all nan; searching for nearest not nan ...')
            sst_sub, lat_fix, lon_fix = search_nearest_not_nan(sst, lat_ind, lon_ind, distance=psm_params_dict['search_dist'])
            lat_ind_fix = lat_ind + lat_fix
            lon_ind_fix = lon_ind + lon_fix
            print(f'PRYSM >>> Target: ({lat_obs}, {lon_obs}); Found: ({lat_model[lat_ind_fix, lon_ind_fix]:.2f}, {lon_model[lat_ind_fix, lon_ind_fix]:.2f})')
        else:
            lat_ind_fix = lat_ind
            lon_ind_fix = lon_ind

        sss = prior_vars_dict['sss']
        if sss is not None:
            sss_sub = np.array(sss[:, lat_ind, lon_ind])
            if np.all(np.isnan(sss_sub)):
                print(f'PRYSM >>> sss all nan; searching for nearest not nan ...')
                sss_sub, lat_fix, lon_fix = search_nearest_not_nan(sss, lat_ind, lon_ind, distance=psm_params_dict['search_dist'])
                lat_ind_fix = lat_ind + lat_fix
                lon_ind_fix = lon_ind + lon_fix
                print(f'PRYSM >>> Target: ({lat_obs}, {lon_obs}); Found: ({lat_model[lat_ind_fix, lon_ind_fix]:.2f}, {lon_model[lat_ind_fix, lon_ind_fix]:.2f})')
            else:
                lat_ind_fix = lat_ind
                lon_ind_fix = lon_ind
        else:
            sss_sub = None

        d18Osw = prior_vars_dict['d18Osw']
        if d18Osw is not None:
            d18Osw_sub = np.array(d18Osw[:, lat_ind, lon_ind])
            if np.all(np.isnan(d18Osw_sub)):
                print(f'PRYSM >>> d18Osw all nan; searching for nearest not nan ...')
                d18Osw_sub, lat_fix, lon_fix = search_nearest_not_nan(d18Osw, lat_ind, lon_ind, distance=psm_params_dict['search_dist'])
                lat_ind_fix = lat_ind + lat_fix
                lon_ind_fix = lon_ind + lon_fix
                print(f'PRYSM >>> Target: ({lat_obs}, {lon_obs}); Found: ({lat_model[lat_ind_fix, lon_ind_fix]:.2f}, {lon_model[lat_ind_fix, lon_ind_fix]:.2f})')
            else:
                lat_ind_fix = lat_ind
                lon_ind_fix = lon_ind
        else:
            d18Osw_sub = None

        species = psm_params_dict['species']
        b1 = psm_params_dict['b1']
        b2 = psm_params_dict['b2']
        b3 = psm_params_dict['b3']
        b4 = psm_params_dict['b4']
        b5 = psm_params_dict['b5']

        pseudo_value = coral.pseudocoral(lat_obs, lon_obs, sst_sub, sss=sss_sub,
                                         d18O=d18Osw_sub, species=species,
                                         b1=b1, b2=b2, b3=b3, b4=b4, b5=b5)

        if psm_params_dict['seasonality'] == list(range(1, 13)):
            pseudo_value, pseudo_time = LMRt.utils.annualize_var(pseudo_value, time_model)
        else:
            pseudo_time = time_model

        res = {
            'pseudo_time': pseudo_time,
            'pseudo_value': pseudo_value,
            'lat_ind': lat_ind_fix,
            'lon_ind': lon_ind_fix,
        }

        return res

    def run_psm_for_coral_SrCa():
        sst = np.array(prior_vars_dict['sst']) - 273.15  # convert to degC
        a = psm_params_dict['a']
        b = psm_params_dict['b']
        seed = psm_params_dict['seed']

        sst_sub = np.array(sst[:, lat_ind, lon_ind])
        if np.all(np.isnan(sst_sub)):
            print(f'PRYSM >>> sst all nan; searching for nearest not nan ...')
            sst_sub, lat_fix, lon_fix = search_nearest_not_nan(sst, lat_ind, lon_ind, distance=psm_params_dict['search_dist'])
            lat_ind_fix = lat_ind + lat_fix
            lon_ind_fix = lon_ind + lon_fix
            print(f'PRYSM >>> Target: ({lat_obs}, {lon_obs}); Found: ({lat_model[lat_ind_fix, lon_ind_fix]:.2f}, {lon_model[lat_ind_fix, lon_ind_fix]:.2f})')
        else:
            lat_ind_fix = lat_ind
            lon_ind_fix = lon_ind

        pseudo_value = coral.sensor_SrCa(sst_sub, a, b, seed)

        if psm_params_dict['seasonality'] == list(range(1, 13)):
            pseudo_value, pseudo_time = LMRt.utils.annualize_var(pseudo_value, time_model)
        else:
            pseudo_time = time_model

        res = {
            'pseudo_time': pseudo_time,
            'pseudo_value': pseudo_value,
            'lat_ind': lat_ind_fix,
            'lon_ind': lon_ind_fix,
        }

        return res

    def run_psm_for_ice_d18O():
        tas = prior_vars_dict['tas']
        pr = prior_vars_dict['pr']
        psl = prior_vars_dict['psl']
        d18Opr = prior_vars_dict['d18Opr']

        if tas is None or pr is None or psl is None or d18Opr is None:
            raise TypeError

        tas_sub = np.array(tas[:, lat_ind, lon_ind])
        nproc = psm_params_dict['nproc']
        if elev_obs is not None and elev_model is not None:
            alt_diff = elev_obs - elev_model[lat_ind, lon_ind]
            tas_sub_old = np.copy(tas_sub)
            tas_sub += alt_diff*(-6/1000)  # bias correction for elevation difference
            if verbose:
                print(f'PRYSM >>> elev_obs: {elev_obs:.2f}, elev_model: {elev_model[lat_ind, lon_ind]:.2f}')
                print(f'PRYSM >>> mean(tas): {np.mean(tas_sub_old)} -> {np.mean(tas_sub)}')

        pr_sub = np.array(pr[:, lat_ind, lon_ind])
        psl_sub = np.array(psl[:, lat_ind, lon_ind])

        # annualize the data
        tas_ann, year_int = LMRt.utils.annualize_var(tas_sub, time_model)
        psl_ann, year_int = LMRt.utils.annualize_var(psl_sub, time_model)
        pr_ann, year_int = LMRt.utils.annualize_var(pr_sub, time_model)

        # sensor model
        d18O_ice = icecore.ice_sensor(time_model, d18Opr, pr, alt_diff=alt_diff)
        # diffuse model
        ice_diffused = icecore.ice_archive(d18O_ice[:, lat_ind, lon_ind], pr_ann, tas_ann, psl_ann, nproc=nproc)

        pseudo_value = ice_diffused[::-1]
        pseudo_time = year_int

        res = {
            'pseudo_time': pseudo_time,
            'pseudo_value': pseudo_value,
            'd18O_ice': d18O_ice[:, lat_ind, lon_ind],
            'ice_diffused': ice_diffused,
        }

        return res

    def run_psm_for_tree_trw():
        tas = prior_vars_dict['tas']
        pr = prior_vars_dict['pr']

        if tas is None or pr is None:
            raise TypeError

        T1 = psm_params_dict['T1']
        T2 = psm_params_dict['T2']
        M1 = psm_params_dict['M1']
        M2 = psm_params_dict['M2']
        normalize = psm_params_dict['normalize']
        Rlib_path = psm_params_dict['Rlib_path']
        pid = psm_params_dict['pid']
        tas_corrected = psm_params_dict['tas_corrected']
        pr_corrected = psm_params_dict['pr_corrected']
        bias_correction = psm_params_dict['bias_correction']
        ref_tas = psm_params_dict['ref_tas']
        ref_pr = psm_params_dict['ref_pr']
        ref_time = psm_params_dict['ref_time']
        ref_lat = psm_params_dict['ref_lat']
        ref_lon = psm_params_dict['ref_lon']
        seed = psm_params_dict['seed']
        lapse_rate = psm_params_dict['lapse_rate']

        if verbose:
            print(f'PRYSM >>> Using R libs from: {Rlib_path}')
            print(f'PRYSM >>> T1={T1:.3f}, T2={T2:.3f}, M1={M1:.3f}, M2={M2:.3f}')

        syear, eyear = int(np.floor(time_model[0])), int(np.floor(time_model[-1]))  # start and end year
        nyr = eyear - syear + 1
        phi = lat_obs

        tas_sub = np.array(tas[:, lat_ind, lon_ind])
        pr_sub = np.array(pr[:, lat_ind, lon_ind])

        if bias_correction:
            pr_sub_old = np.copy(pr_sub)
            tas_sub_old = np.copy(tas_sub)

            if verbose:
                print('PRYSM >>> Performing multivariate bias correction ...')

            if tas_corrected is None:
                # get the closest grid point in the reference field
                ref_lat_ind, ref_lon_ind = LMRt.utils.find_closest_loc(ref_lat, ref_lon, lat_obs, lon_obs)

                ref_tas_sub = ref_tas[:, ref_lat_ind, ref_lon_ind]
                ref_pr_sub = ref_pr[:, ref_lat_ind, ref_lon_ind]

                tas_sub, pr_sub = LMRt.utils.mbc(
                    tas_sub, pr_sub, time_model, ref_tas_sub, ref_pr_sub, ref_time,
                    Rlib_path=Rlib_path, seed=seed,
                )
            else:
                tas_sub = tas_corrected[pid]
                pr_sub = pr_corrected[pid]

            if verbose:
                print(f'PRYSM >>> tas_mean: {np.nanmean(tas_sub_old)} -> {np.nanmean(tas_sub)}')
                print(f'PRYSM >>> pr_mean: {np.nanmean(pr_sub_old)} -> {np.nanmean(pr_sub)}')


        if verbose:
            print(f'PRYSM >>> tas: m={np.nanmean(tas_sub)-273.15:.2f}, std={np.nanstd(tas_sub):.2f}; pr: m={np.nanmean(pr_sub*3600*24*30):.2f}, std={np.nanstd(pr_sub*3600*24*30):.2f}')

        vsl_result = tree.vslite(
            syear, eyear, phi, tas_sub, pr_sub,
            Rlib_path=Rlib_path, T1=T1, T2=T2, M1=M1, M2=M2,
            normalize=normalize,
        )
        pseudo_value = vsl_result['trw_org']
        pseudo_time = np.linspace(syear, eyear, nyr)

        res = {
            'pseudo_time': pseudo_time,
            'pseudo_value': pseudo_value,
            'vsl_result': vsl_result,
        }

        return res

    def run_psm_for_tree_mxd():
        tas = prior_vars_dict['tas']
        SNR = psm_params_dict['SNR_tree.mxd']
        seed = psm_params_dict['seed']

        if tas is None:
            raise TypeError

        tas_sub = np.array(tas[:, lat_ind, lon_ind])
        if verbose:
            print(f'PRYSM >>> tas: m={np.nanmean(tas_sub):.2f}, std={np.nanstd(tas_sub)}')

        tas_JJA, pseudo_time = LMRt.utils.seasonal_var(tas_sub, time_model, avgMonths=[6, 7, 8])

        pseudo_value = tree.mxd(tas_JJA, lon_model[lon_ind], SNR=SNR, seed=seed)

        res = {
            'pseudo_time': pseudo_time,
            'pseudo_value': pseudo_value,
        }

        return res

    def run_psm_for_lake_varve():
        tas = prior_vars_dict['tas']
        H = psm_params_dict['H']
        shape = psm_params_dict['shape']
        mean = psm_params_dict['mean']
        SNR = psm_params_dict['SNR_lake.varve']
        seed = psm_params_dict['seed']
        if tas is None:
            raise TypeError

        tas_sub = np.array(tas[:, lat_ind, lon_ind])
        if verbose:
            print(f'PRYSM >>> tas: m={np.nanmean(tas_sub)-273.15:.2f}, std={np.nanstd(tas_sub)}')

        tas_JJA, pseudo_time = LMRt.utils.seasonal_var(tas_sub, time_model, avgMonths=[6, 7, 8])

        varve_res = lake.simpleVarveModel(tas_JJA, H, shape=shape, mean=mean, SNR=SNR, seed=seed)
        varves = varve_res['varves']
        pseudo_value = np.array(varves)[0]

        res = {
            'pseudo_time': pseudo_time,
            'pseudo_value': pseudo_value,
            'varve_res': varve_res,
        }

        return res


    def run_linear_psm():
        if psm_params_dict['Seasonality'] is None:
            pseudo_value, pseudo_time = np.nan, np.nan
        else:
            avgMonths = psm_params_dict['Seasonality']
            tas = prior_vars_dict['tas']
            tas_sub = np.array(tas[:, lat_ind, lon_ind])
            tas_ann, pseudo_time = LMRt.utils.seasonal_var(tas_sub, time_model, avgMonths=avgMonths)

            slope = psm_params_dict['slope']
            intercept = psm_params_dict['intercept']
            pseudo_value = slope*tas_ann + intercept

        res = {
            'pseudo_time': pseudo_time,
            'pseudo_value': pseudo_value,
        }

        return res

    def run_bilinear_psm():
        if psm_params_dict['Seasonality'] is None:
            pseudo_value, pseudo_time = np.nan, np.nan
        else:
            avgMonths_T, avgMonths_P  = psm_params_dict['Seasonality']
            tas = prior_vars_dict['tas']
            pr = prior_vars_dict['pr']
            tas_sub = np.array(tas[:, lat_ind, lon_ind])
            tas_ann, pseudo_time = LMRt.utils.seasonal_var(tas_sub, time_model, avgMonths=avgMonths_T)
            pr_sub = np.array(pr[:, lat_ind, lon_ind])
            pr_ann, pseudo_time = LMRt.utils.seasonal_var(pr_sub, time_model, avgMonths=avgMonths_P)

            slope_temperature = psm_params_dict['slope_temperature']
            slope_moisture = psm_params_dict['slope_moisture']
            intercept = psm_params_dict['intercept']
            pseudo_value = slope_temperature*tas_ann + slope_moisture*pr_ann + intercept

        res = {
            'pseudo_time': pseudo_time,
            'pseudo_value': pseudo_value,
        }

        return res

    # run PRYSM
    if verbose:
        print(f'PRYSM >>> forward with {psm_name} ...')

    prior_vars_dict = {
        'tas': None,
        'pr': None,
        'psl': None,
        'd18Opr': None,
        'd18Osw': None,
        'sst': None,
        'sss': None,
    }
    prior_vars_dict.update(prior_vars)

    psm_params_dict = {
        # general
        'seasonality': list(range(1, 13)),
        'search_dist': 3,
        'seed': 0,
        'lapse_rate': -6*1e-3,
        'elev_correction': False,

        # for coral.d18O
        'species': 'default',
        'b1': 0.3007062,
        'b2': 0.2619054,
        'b3': 0.436509,
        'b4': 0.1552032,
        'b5': 0.15,

        # for coral.SrCa
        'a': None,
        'b': 10.553,

        # for ice.d18O
        'nproc': 8,

        # for vslite
        'T1': 8,
        'T2': 23,
        'M1': 0.01,
        'M2': 0.05,
        'normalize': False,
        'bias_correction': False,
        'tas_corrected': None,
        'pr_corrected': None,
        'pid': None,
        'ref_tas': None,
        'ref_pr': None,
        'ref_time': None,
        'ref_lat': None,
        'ref_lon': None,
        'Rlib_path': '/Library/Frameworks/R.framework/Versions/3.6/Resources/library',

        # for tree.mxd
        'SNR_tree.mxd': 1,

        # for lake.varve
        'H': 0.5,  # Hurst index
        'shape': 1.5,
        'mean': 1,
        'SNR_lake.varve': 0.25,

        # for linear
        'Seasonality': None,
        'slope': np.nan,
        'intercept': np.nan,

        # for bilinear
        'Seasonality': None,
        'slope_temperature': np.nan,
        'slope_moisture': np.nan,
        'intercept': np.nan,
    }
    psm_params_dict.update(psm_params)

    if latlon_ind_dict is None:
        if latlon_search_mode is None and len(np.shape(lat_model)) == 1:
            latlon_search_mode = 'latlon'
        else:
            latlon_search_mode = 'mesh'
        lat_ind, lon_ind = LMRt.utils.find_closest_loc(lat_model, lon_model, lat_obs, lon_obs, mode=latlon_search_mode)
    else:
        # load precalculated lat/lon indices
        lat_ind, lon_ind = latlon_ind_dict[record_id]

    if verbose:
        if len(np.shape(lat_model)) == 1:
            print(f'PRYSM >>> Target: ({lat_obs}, {lon_obs}); Found: ({lat_model[lat_ind]:.2f}, {lon_model[lon_ind]:.2f}); lat_ind: {lat_ind}, lon_ind: {lon_ind}')
        elif len(np.shape(lat_model)) == 2:
            print(f'PRYSM >>> Target: ({lat_obs}, {lon_obs}); Found: ({lat_model[lat_ind, lon_ind]:.2f}, {lon_model[lat_ind, lon_ind]:.2f}); lat_ind: {lat_ind}, lon_ind: {lon_ind}')

    psm_func = {
        'prysm.coral.d18O': run_psm_for_coral_d18O,
        'prysm.coral.SrCa': run_psm_for_coral_SrCa,
        'prysm.ice.d18O': run_psm_for_ice_d18O,
        'prysm.vslite': run_psm_for_tree_trw,
        'prysm.tree.mxd': run_psm_for_tree_mxd,
        'prysm.lake.varve': run_psm_for_lake_varve,
        'linear': run_linear_psm,
        'bilinear': run_bilinear_psm,
    }

    res = psm_func[psm_name]()

    if verbose:
        pseudo_value, pseudo_time = res['pseudo_value'], res['pseudo_time']
        mean_value = np.nanmean(pseudo_value)
        std_value = np.nanstd(pseudo_value)
        print(f'PRYSM >>> shape: {np.shape(pseudo_value)}')
        print(f'PRYSM >>> mean: {mean_value:.2f}; std: {std_value:.2f}')

    return res


def search_nearest_not_nan(field, lat_ind, lon_ind, distance=3):
    fix_sum = []
    lat_fix_list = []
    lon_fix_list = []
    for lat_fix, lon_fix in itertools.product(np.arange(-distance, distance+1), np.arange(-distance, distance+1)):
        lat_fix_list.append(lat_fix)
        lon_fix_list.append(lon_fix)
        fix_sum.append(np.abs(lat_fix)+np.abs(lon_fix))

    lat_fix_list = np.array(lat_fix_list)
    lon_fix_list = np.array(lon_fix_list)

    sort_i = np.argsort(fix_sum)

    for lat_fix, lon_fix in zip(lat_fix_list[sort_i], lon_fix_list[sort_i]):
        target = np.array(field[:, lat_ind+lat_fix, lon_ind+lon_fix])
        if np.all(np.isnan(target)):
            continue
        else:
            print(f'PRYSM >>> Found not nan with (lat_fix, lon_fix): ({lat_fix}, {lon_fix})')
            return target, lat_fix, lon_fix

    print(f'PRYSM >>> Fail to find value not nan!')
    return np.nan, np.nan, np.nan

