from collections import defaultdict
import math
import numpy as np
from numpy import ma


def find_neighbors(pindex, triang):  # zou recursief moeten kunne
    return triang.vertex_neighbor_vertices[1][
        triang.vertex_neighbor_vertices[0][pindex] : triang.vertex_neighbor_vertices[0][
            pindex + 1
        ]
    ]


def find_neighbors2(index, triang, depth):
    buren = np.array([index])  # list van een set -> verzamelt de unieke
    for _ in range(depth):
        for buur in buren:
            buren_temp = np.array([])
            temp = find_neighbors(int(buur), triang)
            for j in temp:
                if j in buren:
                    None
                else:
                    buren_temp = np.append(buren_temp, int(j))
            buren = np.append(buren, buren_temp)
    buren = np.delete(buren, 0)
    return buren


def Squat(h, T, V_max, LWL, WWL, ukc, WVPI):
    Gamma_water = 1025
    b = 9 * WWL
    g = 9.81
    ghv2 = g * h / (V_max ** 2)
    squat_max = h - T - ukc
    CB = WVPI / (LWL * WWL * T * Gamma_water)
    AsAc = (WWL * T) / (b * h - WWL * T)
    RH = (b * h - WWL * T) / (b + 2 * h + 2 * T + WWL)

    VhV1 = (
        1.002
        + 0.005 * (np.sqrt(WWL * T) / RH)
        - 0.1159 * (np.sqrt(WWL * T) / RH) ** 2
        + 0.0191 * (np.sqrt(WWL * T) / RH) ** 3
    )
    V1Vinf = ((np.exp(ghv2) - np.exp(-ghv2)) / (np.exp(ghv2) + np.exp(-ghv2))) ** 0.5

    V_grens = V_max * V1Vinf * VhV1
    V_squat_max = np.zeros(len(h))
    V = np.zeros(len(h))
    for i in range(len(h)):
        V_squat_max[i] = (
            0
            if squat_max[i] < 0
            else (squat_max[i] * 30 / CB / (AsAc[i] ** (2 / 3))) ** (1 / 2.08)
        )
        V[i] = V_grens[i] if V_squat_max[i] > V_grens[i] else V_squat_max[i]

    return V


def inbetweenpoints(start, stop, LL, tria):
    nodes = [start, stop]
    for L in range(1, LL):
        L = L + 1
        NB = np.array(find_neighbors2(start, tria, L - 1), dtype=int)
        if stop not in NB:
            add_nodes = set(find_neighbors2(stop, tria, L - 1)) & set(
                find_neighbors2(start, tria, L - 1)
            )
            add_nodes = np.array(list(add_nodes), dtype=int)
            nodes = np.concatenate((nodes, add_nodes))
    return nodes


def haversine(coord1, coord2):
    R = 6372800  # https://janakiev.com/blog/gps-points-distance-python/
    lat1, lon1 = coord1
    lat2, lon2 = (
        coord2
    )  # use the Haversine function to determine the distance between two points in the WGS84 coordinate system

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = (
        math.sin(dphi / 2) ** 2
        + math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2
    )

    return 2 * R * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def costfunction_timeseries(edge, V_max, WD_min, flow, WVPI, L, tria):
    xfrom = flow.nodes[edge[0]][1]
    yfrom = flow.nodes[edge[0]][0]
    xto = flow.nodes[edge[1]][1]
    yto = flow.nodes[edge[1]][0]
    IB = inbetweenpoints(edge[0], edge[1], L, tria)
    v_w = flow.v[IB[0]]
    u_w = flow.u[IB[0]]
    WD_W = flow.WD[IB[0]]
    for i in range(1, len(IB)):
        v_w = v_w + flow.v[IB[i]]
        u_w = u_w + flow.u[IB[i]]

        # WD_W = WD_W + flow.WD[IB[i]]
        WD_W = np.minimum(WD_W, flow.WD[IB[i]])

    # WD_W= WD_W / len(IB)
    v_w = v_w / len(IB)
    u_w = u_w / len(IB)
    U_w = (u_w ** 2 + v_w ** 2) ** 0.5

    vship = Squat(WD_W, WD_min, V_max, flow.LWL, flow.WWL, flow.ukc, WVPI)

    alpha1 = np.arctan2((yto - yfrom), (xto - xfrom))
    alpha2 = np.arctan2(v_w, u_w) - alpha1

    s_t = (U_w * np.cos(alpha2)) + (vship ** 2 - (U_w * np.sin(alpha2)) ** 2) ** 0.5

    u_t = np.cos(alpha1) * (s_t)
    v_t = np.sin(alpha1) * (s_t)

    L = haversine((yfrom, xfrom), (yto, xto))
    U_t = (u_t ** 2 + v_t ** 2) ** 0.5
    t = L / U_t

    t[U_t == np.inf] = np.inf
    t[np.isnan(t)] = np.inf
    t[WD_W < WD_min + flow.ukc] = np.inf
    t[WD_W < WD_min + flow.ukc] = np.inf
    t[(U_w * np.sin(alpha2)) ** 2 > vship ** 2] = np.inf
    t[s_t < 0] = np.inf
    return np.array(t)


def costfunction_spaceseries(edge, V_max, WD_min, flow, WVPI, L, tria):
    xfrom = flow.nodes[edge[0]][1]
    yfrom = flow.nodes[edge[0]][0]
    xto = flow.nodes[edge[1]][1]
    yto = flow.nodes[edge[1]][0]
    IB = inbetweenpoints(edge[0], edge[1], L, tria)
    v_w = flow.v[IB[0]]
    u_w = flow.u[IB[0]]
    WD_W = flow.WD[IB[0]]
    for i in range(1, len(IB)):
        v_w = v_w + flow.v[IB[i]]
        u_w = u_w + flow.u[IB[i]]

        # WD_W = WD_W + flow.WD_W[IB[i]]
        WD_W = np.minimum(WD_W, flow.WD[IB[i]])

    # WD_W= WD_W / len(IB)
    v_w = v_w / len(IB)
    u_w = u_w / len(IB)
    U_w = (u_w ** 2 + v_w ** 2) ** 0.5

    vship = Squat(WD_W, WD_min, V_max, flow.LWL, flow.WWL, flow.ukc, WVPI)

    alpha1 = np.arctan2((yto - yfrom), (xto - xfrom))
    alpha2 = np.arctan2(v_w, u_w) - alpha1

    s_t = (U_w * np.cos(alpha2)) + (vship ** 2 - (U_w * np.sin(alpha2)) ** 2) ** 0.5

    u_t = np.cos(alpha1) * (s_t)
    v_t = np.sin(alpha1) * (s_t)

    L = haversine((yfrom, xfrom), (yto, xto))
    U_t = (u_t ** 2 + v_t ** 2) ** 0.5
    t = L / U_t

    t[U_t == np.inf] = np.inf
    t[np.isnan(t)] = np.inf
    t[WD_W < WD_min + flow.ukc] = np.inf
    t[WD_W < WD_min + flow.ukc] = np.inf
    t[(U_w * np.sin(alpha2)) ** 2 > vship ** 2] = np.inf
    t[s_t < 0] = np.inf
    t[t != np.inf] = L

    return np.array(t)


def nodes_on_land_None(nodes, u, v, WD):
    """Standard function that returns itself"""
    return nodes, u, v, WD
