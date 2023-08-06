"""This module contains methods for performing and visualizing common beam
diagnostics"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import scipy.constants as ct

import aptools.data_analysis.beam_diagnostics as bd
from aptools.data_handling.reading import read_beam
from aptools.plotting.plot_types import scatter_histogram


aptools_rc_params = {'axes.linewidth': 0.5,
                     'axes.labelsize': 8,
                     'xtick.major.size': 2,
                     'ytick.major.size': 2,
                     'xtick.major.width': 0.5,
                     'ytick.major.width': 0.5,
                     'xtick.labelsize': 8,
                     'ytick.labelsize': 8,
                     'xtick.direction': 'in',
                     'ytick.direction': 'in',
                     'xtick.top': True,
                     'ytick.right': True,
                     'legend.borderaxespad': 1}


def phase_space_overview_from_file(code_name, file_path, **kwargs):
    x, y, z, px, py, pz, q = read_beam(code_name, file_path, **kwargs)
    phase_space_overview(x, y, z, px, py, pz, q)


def phase_space_overview(x, y, z, px, py, pz, q):
    em_x = bd.normalized_transverse_rms_emittance(x, px, w=q) * 1e6
    em_y = bd.normalized_transverse_rms_emittance(y, py, w=q) * 1e6
    a_x, b_x, g_x = bd.twiss_parameters(x, px, pz, w=q)
    a_y, b_y, g_y = bd.twiss_parameters(y, py, pz, w=q)
    s_x = bd.rms_size(x, w=q)
    s_y = bd.rms_size(y, w=q)
    em_l = bd.longitudinal_rms_emittance(z, px, py, pz, w=q) * 1e6
    dz = z - np.average(z, weights=q)
    s_z = bd.rms_length(z, w=q)
    s_g = bd.relative_rms_energy_spread(pz, py, pz, w=q)
    s_g_sl, w_sl, sl_ed = bd.relative_rms_slice_energy_spread(z, px, py, pz,
                                                              w=q, n_slices=10)
    s_g_sl_av = np.average(s_g_sl, weights=w_sl)
    c_prof, _ = bd.current_profile(z, q, n_slices=50)
    c_peak = max(abs(c_prof))/1e3  # kA
    # s_g_sl_c = s_g_sl[int(len(s_g_sl)/2)]

    # make plot
    plt.figure(figsize=(8, 3))
    with plt.rc_context(aptools_rc_params):
        # x - px
        ax_1 = plt.subplot(131)
        scatter_histogram(x*1e6, px)
        plt.xlabel("x [$\\mu m$]")
        plt.ylabel("$p_x \\ \\mathrm{[m_ec^2/e]}$")
        plt.text(0.1, 0.9, '$\\epsilon_{n,x} = $'
                 + '{}'.format(np.around(em_x, 3))
                 + '$\\ \\mathrm{\\pi \\ \\mu m \\ rad}$',
                 transform=ax_1.transAxes, fontsize=8)
        plt.text(0.1, 0.8, '$\\beta_{x} = $' + '{}'.format(np.around(b_x, 3))
                 + 'm', transform=ax_1.transAxes, fontsize=8)
        plt.text(0.1, 0.7, '$\\alpha_{x} = $' + '{}'.format(np.around(a_x, 3)),
                 transform=ax_1.transAxes, fontsize=8)
        plt.text(0.1, 0.6, '$\\sigma_{x} = $'
                 + '{}'.format(np.around(s_x*1e6, 3))
                 + '$\\ \\mathrm{\\mu m}$', transform=ax_1.transAxes,
                 fontsize=8)
        # y - py
        ax_2 = plt.subplot(132)
        scatter_histogram(y * 1e6, py)
        plt.xlabel("y [$\\mu m$]")
        plt.ylabel("$p_y \\ \\mathrm{[m_ec^2/e]}$")
        plt.text(0.1, 0.9, '$\\epsilon_{n,y} = $'
                 + '{}'.format(np.around(em_y, 3))
                 + '$\\ \\mathrm{\\pi \\ \\mu m \\ rad}$',
                 transform=ax_2.transAxes, fontsize=8)
        plt.text(0.1, 0.8, '$\\beta_{y} = $' + '{}'.format(np.around(b_y, 3))
                 + 'm', transform=ax_2.transAxes, fontsize=8)
        plt.text(0.1, 0.7, '$\\alpha_{y} = $' + '{}'.format(np.around(a_y, 3)),
                 transform=ax_2.transAxes, fontsize=8)
        plt.text(0.1, 0.6, '$\\sigma_{y} = $'
                 + '{}'.format(np.around(s_y*1e6, 3))
                 + '$\\ \\mathrm{\\mu m}$', transform=ax_2.transAxes,
                 fontsize=8)
        # z - pz
        ax_3 = plt.subplot(133)
        scatter_histogram(dz / ct.c * 1e15, pz)
        plt.xlabel("$\\Delta z$ [fs]")
        plt.ylabel("$p_z \\ \\mathrm{[m_ec^2/e]}$")
        plt.text(0.1, 0.9, '$\\epsilon_{L} = $'
                 + '{}'.format(np.around(em_l, 3))
                 + '$\\ \\mathrm{\\pi \\ \\mu m}$', transform=ax_3.transAxes,
                 fontsize=8)
        plt.text(0.1, 0.8, '$\\sigma_\\gamma/\\gamma=$'
                 + '{}'.format(np.around(s_g*1e2, 3)) + '$\\%$',
                 transform=ax_3.transAxes, fontsize=8)
        plt.text(0.1, 0.7, '$\\sigma^s_\\gamma/\\gamma=$'
                 + '{}'.format(np.around(s_g_sl_av*1e2, 3)) + '$\\%$',
                 transform=ax_3.transAxes, fontsize=8)
        plt.text(0.1, 0.6, '$\\sigma_z=$'
                 + '{}'.format(np.around(s_z/ct.c*1e15, 3)) + ' fs',
                 transform=ax_3.transAxes, fontsize=8)
        plt.text(0.1, 0.5, '$I_{peak}=$'
                 + '{}'.format(np.around(c_peak, 2)) + ' kA',
                 transform=ax_3.transAxes, fontsize=8)
        plt.tight_layout()
    plt.show()


def slice_analysis(x, y, z, px, py, pz, q, n_slices=10, len_slice=None,
                   left=0.125, right=0.875, top=0.98, bottom=0.11,
                   add_labels=False):
    # analyze beam
    current_prof, z_edges = bd.current_profile(z, q, n_slices=n_slices,
                                               len_slice=len_slice)
    slice_ene, *_ = bd.energy_profile(
        z, px, py, pz, w=q, n_slices=n_slices, len_slice=len_slice)
    slice_ene_sp, *_ = bd.relative_rms_slice_energy_spread(
        z, px, py, pz, w=q, n_slices=n_slices, len_slice=len_slice)
    params = bd.slice_twiss_parameters(
        z, x, px, pz, w=q, n_slices=n_slices, len_slice=len_slice)
    alpha_x = params[0]
    beta_x = params[1]
    params = bd.slice_twiss_parameters(
        z, y, py, pz, w=q, n_slices=n_slices, len_slice=len_slice)
    alpha_y = params[0]
    beta_y = params[1]
    slice_em_x, *_ = bd.normalized_transverse_rms_slice_emittance(
        z, x, px, w=q, n_slices=n_slices, len_slice=len_slice)
    slice_em_y, *_ = bd.normalized_transverse_rms_slice_emittance(
        z, y, py, w=q, n_slices=n_slices, len_slice=len_slice)
    len_fwhm = bd.fwhm_length(z, q, n_slices=n_slices, len_slice=len_slice)
    ene_sp_tot = bd.relative_rms_energy_spread(px, py, pz, w=q)

    # perform operations
    gamma = np.sqrt(1 + px**2 + py**2 + pz**2)
    ene = gamma * ct.m_e*ct.c**2/ct.e * 1e-9  # GeV
    z_center = np.average(z, weights=q)
    dz = z_edges[1] - z_edges[0]
    slice_z = (z_edges[1:] - dz/2 - z_center) * 1e6  # micron
    current_prof = np.abs(current_prof) * 1e-3  # kA
    peak_current = max(current_prof)
    len_fwhm *= 1e15/ct.c  # fs
    slice_ene *= ct.m_e*ct.c**2/ct.e * 1e-9  # GeV
    slice_ene_sp *= 1e2  # %
    ene_sp_tot *= 1e2  # %
    slice_em_x *= 1e6  # micron
    slice_em_y *= 1e6  # micron
    max_beta = max(beta_x)
    if max_beta <= 0.1:
        beta_units = 'mm'
        beta_x *= 1e3
        beta_y *= 1e3
    else:
        beta_units = 'm'
    max_ene = max(ene)
    if max_ene <= 1:
        ene_units = 'MeV'
        ene *= 1e3
    else:
        ene_units = 'GeV'
    ene_mean = np.average(ene, weights=q)

    # make plot
    fig = plt.figure(figsize=(4, 3.5))
    gs = gridspec.GridSpec(3, 2, height_ratios=[2.5, 1, 1],
                           width_ratios=[1, 0.02], hspace=0.1, wspace=0.05,
                           figure=fig, left=left, right=right,
                           top=top, bottom=bottom)
    leg_frac = 0.25  # space to reserve for legend

    with plt.rc_context(aptools_rc_params):
        ax_or = plt.subplot(gs[0])
        pscatt = scatter_histogram((z-z_center)*1e6, ene, bins=300,
                                   weights=np.abs(q)*1e15)
        plt.ylabel('Energy [{}]'.format(ene_units))
        plt.tick_params(axis='x', which='both', labelbottom=False)
        params_text = ('$\\langle E \\rangle = '
                       + '{:0.1f}$ {}\n'.format(ene_mean, ene_units)
                       + '$\\sigma_\\mathrm{E,rel}='
                       + '{:0.1f}$ %\n'.format(ene_sp_tot)
                       + '$I_\\mathrm{peak}='
                       + '{:0.1f}$ kA\n'.format(peak_current)
                       + '$\\tau_\\mathrm{FWHM}='
                       + '{:0.1f}$ fs'.format(len_fwhm))
        plt.text(0.95, 0.95, params_text, transform=ax_or.transAxes,
                 fontsize=6, horizontalalignment='right',
                 verticalalignment='top')
        if add_labels:
            plt.text(0.03, 0.05, '(a)', transform=ax_or.transAxes, fontsize=6,
                     horizontalalignment='left', verticalalignment='bottom')

        ylim = list(plt.ylim())
        ylim[0] -= (ylim[1] - ylim[0])/3
        plt.ylim(ylim)

        z_or = ax_or.get_zorder()
        pos = list(ax_or.get_position().bounds)
        pos[3] /= 5
        ax_or.patch.set_alpha(0)
        xlim = plt.xlim()

        ax = fig.add_axes(pos)
        ax.set_zorder(z_or-1)
        plt.plot(slice_z, current_prof, c='k', lw=0.5, alpha=0.5)
        plt.fill_between(slice_z, current_prof, facecolor='tab:gray',
                         alpha=0.3)
        ax.spines['left'].set_position('zero')
        ax.spines['left'].set_color('tab:grey')
        ax.tick_params(axis='y', colors='tab:grey', labelsize=6,
                       direction="in", pad=-4)
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.yaxis.set_ticks_position('left')
        ax.xaxis.set_ticks_position('bottom')
        plt.tick_params(axis='x', which='both', labelbottom=False)
        for label in ax.yaxis.get_ticklabels():
            label.set_horizontalalignment('left')
            label.set_verticalalignment('bottom')
        plt.xlim(xlim)
        plt.ylabel('I [kA]', color='tab:gray', fontsize=6)

        ax = plt.subplot(gs[1])
        matplotlib.colorbar.Colorbar(ax, pscatt, label='Q [fC]')

        plt.subplot(gs[2])
        l1 = plt.plot(slice_z, slice_ene_sp, lw=1, c='tab:green',
                      label='$\\sigma_\\gamma/\\gamma$')
        plt.ylabel('$\\sigma_\\gamma/\\gamma$ [%]')
        plt.tick_params(axis='x', which='both', labelbottom=False)
        # make room for legend
        ylim = list(plt.ylim())
        ylim[1] += (ylim[1] - ylim[0]) * leg_frac
        plt.ylim(ylim)

        ax = plt.twinx()
        l2 = plt.plot(slice_z, slice_em_x, lw=1, c='tab:blue',
                      label='$\\epsilon_{n,x}$')
        l3 = plt.plot(slice_z, slice_em_y, lw=1, c='tab:orange',
                      label='$\\epsilon_{n,y}$')
        plt.ylabel('$\\epsilon_{n} \\ [\\mathrm{\\mu m}]$')
        # make room for legend
        ylim = list(plt.ylim())
        ylim[1] += (ylim[1] - ylim[0]) * leg_frac
        plt.ylim(ylim)
        lines = l1 + l2 + l3
        labels = [l.get_label() for l in lines]
        plt.legend(lines, labels, fontsize=6, ncol=3, frameon=False,
                   loc='upper right', borderaxespad=0)
        if add_labels:
            plt.text(0.03, 0.95, '(b)', transform=plt.gca().transAxes,
                     fontsize=6, horizontalalignment='left',
                     verticalalignment='top')

        plt.subplot(gs[4])
        l1 = plt.plot(slice_z, beta_x, lw=1, c='tab:blue', label='$\\beta_x$')
        l2 = plt.plot(slice_z, beta_y, lw=1, c='tab:orange',
                      label='$\\beta_y$')
        plt.xlabel('$\\Delta z \\ [\\mathrm{\\mu m}]$')
        plt.ylabel('$\\beta$ [{}]'.format(beta_units))
        # make room for legend
        ylim = list(plt.ylim())
        ylim[1] += (ylim[1] - ylim[0]) * leg_frac
        plt.ylim(ylim)
        plt.twinx()
        l3 = plt.plot(slice_z, alpha_x, lw=1, c='tab:blue', ls='--',
                      label='$\\alpha_x$')
        l4 = plt.plot(slice_z, alpha_y, lw=1, c='tab:orange', ls='--',
                      label='$\\alpha_y$')
        lines = l1 + l2 + l3 + l4
        labels = [l.get_label() for l in lines]
        # make room for legend
        ylim = list(plt.ylim())
        ylim[1] += (ylim[1] - ylim[0]) * leg_frac
        plt.ylim(ylim)
        plt.legend(lines, labels, fontsize=6, ncol=4, frameon=False,
                   loc='upper right', borderaxespad=0)
        if add_labels:
            plt.text(0.03, 0.95, '(c)', transform=plt.gca().transAxes,
                     fontsize=6, horizontalalignment='left',
                     verticalalignment='top')
        plt.ylabel('$\\alpha$')

    plt.show()
