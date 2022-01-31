

user_input = ""
while user_input != "q":
    if user_input == "1":
        ####################################################################
        ############################## TASK 1 ##############################
        ####################################################################
        # constants
        m_per_ft = 0.3048  # 1 ft = 0.3048 m
        ft_per_m = 1 / m_per_ft  # 1 m = 3.28084 ft
        inHg_per_hPa = 29.92 / 1013.25  # 29.92 inHg = 1013.25 hPa
        hPa_per_inHg = 1 / inHg_per_hPa


        # simple helper functions
        # conversion from feet to meters
        def ft_to_m(feet):
            return feet * m_per_ft

        # conversion from meters to feet
        def m_to_ft(meters):
            return meters * ft_per_m

        # conversion from inHg to hPa
        def inHg_to_hPa(inHg):
            return inHg * hPa_per_inHg

        # conversion from hPa to inHg
        def hPa_to_inHg(hPa):
            return hPa * inHg_per_hPa

        # conversion from degrees Celsius to Kelvin
        def celsius_to_kelvin(celsius):
            return celsius + 273.15


        # International Standard atmosphere, values are taken from lecture 4, slide 18
        ISA_p_MSL = 1013.25  # hPa
        ISA_T_MSL = 288.15  # K  (= 273.75 K + 15 K)
        ISA_rel_hum = 0.  # %
        ISA_rho_MSL = 1.225  # kg / m^3
        ISA_T_grad_m = 0.65 / 100  # K / m
        ISA_T_grad_ft = 2. / 1000  # K / ft
        ISA_p_grad_hPa = 1. / 30  # hPa / ft
        ISA_p_grad_inHg = 1. / 1000  # inHg / ft
        ISA_h_tropo_m = 11000.  # m
        ISA_T_tropo = 216.65  # K, up to 50 km

        QNH_STD = ISA_p_MSL  # for convenience


        # compute pressure[hPa] at altitude h_1, given pressure[hPa] at h_0,
        # difference in altitude h_1-h_0[ft] and temperature[K] at h_0
        def compute_p(p_0, delta_h, T_0):
            # use the formula provided on lecture 4, slide 23
            return p_0 * (1 - 0.0065 * ft_to_m(delta_h) / T_0) ** 5.255

        # compute difference[ft] between altitudes h_1 and h_0,
        # provided pressures p(h_1) and p(h_0) [both in hPa] and temperature T(h_0) [K]
        def compute_delta_h(p_1, p_0, T_0):
            # this is the inverse of the formula provided on lecture 4, slide 23
            return m_to_ft(T_0 / 0.0065 * (1 - (p_1 / p_0) ** (1 / 5.255)))

        # compute pressure[hPa] at altitude[ft] according to the ISA
        def compute_ISA_p(alt):
            return compute_p(ISA_p_MSL, alt, ISA_T_MSL)

        # compute altitude[ft] for given pressure[hPa] according to the ISA
        def compute_ISA_alt(p):
            return compute_delta_h(p, ISA_p_MSL, ISA_T_MSL)

        # compute ISA temperature[K] at given altitude[ft]
        def compute_ISA_T(alt):
            if ft_to_m(alt) > ISA_h_tropo_m:
                # temperature in the tropopause (assumed to be constant)
                return ISA_T_tropo
            else:
                # between MSL and tropopause: linear interpolation between fixed temperatures mentioned above
                return ISA_T_MSL + ft_to_m(alt) / ISA_h_tropo_m * (ISA_T_tropo - ISA_T_MSL)

        # compute ISA density[kg/m^3] at given altitude[ft]
        def compute_ISA_rho(alt):
            specific_gas_constant_dry_air = 287.058  # = R [J * kg^-1 * K^-1]; as provided on lecture 3, slide 71
            # rho = p / R / T
            # to account for unit conversion, one has to multiply with 100
            return compute_ISA_p(alt) * 100 / compute_ISA_T(alt) / specific_gas_constant_dry_air

        # compute altitude[ft], given a QNH[hPa] and a pressure[hPa], assuming a temperature of 15 degrees C as MSL
        def compute_altitude_by_QNH(QNH, p):
            return compute_delta_h(p, QNH, ISA_T_MSL)

        # compute height[ft], given a QNH[hPa], a pressure[hPa], and a field elevation[ft],
        # assuming a temperature of 15 degrees C as MSL
        def compute_height_by_QNH(QNH, p, elev):
            return compute_delta_h(p, QNH, ISA_T_MSL) - elev

        # compute altitude[ft], given a QFE[hPa], a pressure[hPa], a field elevation[ft]
        # and a temperature[degrees C] at the aerodrome
        def compute_altitude_by_QFE(QFE, p, elev, T):
            return compute_delta_h(p, QFE, celsius_to_kelvin(T)) + elev

        # compute height[ft], given a QFE[hPa], and a pressure[hPa], and a temperature[degrees C] at the aerodrome
        def compute_height_by_QFE(QFE, p, T):
            return compute_delta_h(p, QFE, celsius_to_kelvin(T))


        # print table according to lecture 4, slide 19
        for i in range(46):
            alt = 1000 * i
            print(alt, "ft =", round(ft_to_m(alt)), "m,",
                  "p =", round(compute_ISA_p(alt), 2), "hPa,",
                  "T =", round(compute_ISA_T(alt), 2), "K,",
                  "rho =", round(compute_ISA_rho(alt), 5), "kg/m^3")
        print("")


        # From here, it's just user interaction
        user_input = ""
        while user_input != "q":
            if user_input == "1":
                alt = float(input("Fuer welche Hoehe soll der Luftdruck bestimmt werden? (Eingabe in ft) > "))
                p_0_text = input("Wie hoch ist der Druck auf MSL? (Eingabe in hPa, keine Eingabe = 1013.25 hPa) > ")
                if p_0_text == "":
                    p_0 = QNH_STD
                else:
                    p_0 = float(p_0_text)
                T_text = input("Wie hoch ist die Temperatur auf MSL? (Eingaben bis 100 werden als Grad C interpretiert, darueber als K; keine Eingabe = 15 Grad C) > ")
                if T_text == "":
                    T = 15
                else:
                    T = float(T_text)
                if T <= 100:
                    T += 273.15
                print("")
                p = compute_p(p_0, alt, T)
                print("Der Luftdruck betraegt", round(p, 2), "hPa")
            if user_input == "2":
                p_1 = float(input("Welcher Luftdruck wurde auf der zu berechnenden Hoehe gemessen? (Eingabe in hPa) > "))
                p_0_text = input("Wie hoch ist der Druck auf MSL? (Eingabe in hPa, keine Eingabe = 1013.25 hPa) > ")
                if p_0_text == "":
                    p_0 = QNH_STD
                else:
                    p_0 = float(p_0_text)
                T_text = input("Wie hoch ist die Temperatur auf MSL? (Eingaben bis 100 werden als  Grad C interpretiert, darueber als K; keine Eingabe = 15 Grad C) > ")
                if T_text == "":
                    T = 15
                else:
                    T = float(T_text)
                if T <= 100:
                    T += 273.15
                print("")
                alt = compute_delta_h(p_1, p_0, T)
                print("Die Hoehe betraegt", round(alt, 2), "ft =", round(ft_to_m(alt), 2), "m")
            if user_input == "3":
                print("Es wird eine Temperatur von 15 Grad C auf MSL angenommen.")
                QNH_text = input("Wie lautet das QNH am Flugplatz? (Eingabe in hPa, keine Eingabe = 1013.25 hPa) > ")
                if QNH_text == "":
                    QNH = QNH_STD
                else:
                    QNH = float(QNH_text)
                p = float(input("Welcher Druck wird am LFZ gemessen? (Eingabe in hPa) > "))
                print("")
                alt = compute_altitude_by_QNH(QNH, p)
                print("Die Altitude betraegt", round(alt, 2), "ft")
            if user_input == "4":
                print("Es wird eine Temperatur von 15 Grad C auf MSL angenommen.")
                QNH_text = input("Wie lautet das QNH am Flugplatz? (Eingabe in hPa, keine Eingabe = 1013.25 hPa) > ")
                if QNH_text == "":
                    QNH = QNH_STD
                else:
                    QNH = float(QNH_text)
                p = float(input("Welcher Druck wird am LFZ gemessen? (Eingabe in hPa) > "))
                elev_text = input("Wie hoch liegt der Flugplatz ueber MSL? (Eingabe in ft, keine Eingabe = 0 ft) > ")
                if elev_text == "":
                    elev = 0
                else:
                    elev = float(elev_text)
                print("")
                h = compute_height_by_QNH(QNH, p, elev)
                print("Die Height betraegt", round(h, 2), "ft")
            if user_input == "5":
                QFE_text = input("Wie lautet das QFE am Flugplatz? (Eingabe in hPa, keine Eingabe = 1013.25 hPa) > ")
                if QFE_text == "":
                    QFE = QNH_STD
                else:
                    QFE = float(QFE_text)
                p = float(input("Welcher Druck wird am LFZ gemessen? (Eingabe in hPa) > "))
                elev_text = input("Wie hoch liegt der Flugplatz ueber MSL? (Eingabe in ft, keine Eingabe = 0 ft) > ")
                if elev_text == "":
                    elev = 0
                else:
                    elev = float(elev_text)
                T_text = input("Wie hoch ist die Temperatur am Flugplatz? (Eingaben bis 100 werden als Grad C interpretiert, darueber als K; keine Eingabe = 15 Grad C) > ")
                if T_text == "":
                    T = 15
                else:
                    T = float(T_text)
                if T <= 100:
                    T += 273.15
                print("")
                alt = compute_altitude_by_QFE(QFE, p, elev, T)
                print("Die Altitude betraegt", round(alt, 2), "ft")
            if user_input == "6":
                QFE_text = input("Wie lautet das QFE am Flugplatz? (Eingabe in hPa, keine Eingabe = 1013.25 hPa) > ")
                if QFE_text == "":
                    QFE = QNH_STD
                else:
                    QFE = float(QFE_text)
                p = float(input("Welcher Druck wird am LFZ gemessen? (Eingabe in hPa) > "))
                elev_text = input("Wie hoch liegt der Flugplatz ueber MSL? (Eingabe in ft, keine Eingabe = 0 ft) > ")
                if elev_text == "":
                    elev = 0
                else:
                    elev = float(elev_text)
                T_text = input("Wie hoch ist die Temperatur am Flugplatz? (Eingaben bis 100 werden als Grad C interpretiert, darueber als K; keine Eingabe = 15 Grad C) > ")
                if T_text == "":
                    T = 15
                else:
                    T = float(T_text)
                if T <= 100:
                    T += 273.15
                print("")
                h = compute_height_by_QFE(QFE, p, elev, T)
                print("Die Height betraegt", round(h, 2), "ft")
            print("")
            print("Aktion waehlen:")
            print("[1] Druck aus Hoehe und Temperatur berechnen")
            print("[2] Hoehe aus Druck und Temperatur berechnen")
            print("[3] Berechnung von Altitude mittels QNH")
            print("[4] Berechnung von Height mittels QNH und Elevation am Flugplatz")
            print("[5] Berechnung von Altitude mittels QFE, Elevation und Temperatur am Flugplatz")
            print("[6] Berechnung von Height mittels QFE, Elevation und Temperatur am Flugplatz")
            print("[q] beenden")
            print("")
            user_input = str(input("> "))
            print("")
    if user_input == "2":
        ####################################################################
        ############################## TASK 2 ##############################
        ####################################################################
        import math  # for sin, cos and sqrt


        # helper functions
        # convert degrees to radians
        def deg_to_rad(deg):
            return deg * math.pi / 180


        # convert radians to degrees
        def rad_to_deg(rad):
            return rad / math.pi * 180


        # compute ground speed[kt], given true air speed[kt] and wind speed[kt]
        # One-dimensional; positive wind speed means tail wind.
        def compute_gs(tas, ws):
            # assume the wind is blowing from behind; then the aircraft gets sped up by that wind speed.
            # if the wind blows opposite to direction of flight (ws negative), it slows the A/C down by that amount.
            # gs = tas + ws
            return tas + ws


        # compute true airspeed[kt], given ground speed[kt] and wind speed[kt]
        # One-dimensional; positive wind speed means tail wind.
        def compute_tas(gs, ws):
            # same formula and logic as above
            return gs - ws


        # compute track[degrees] and ground speed[kt] from heading[degrees], true air speed[kt], wind direction[degrees] and wind speed[kt]
        # Two-dimensional. Wind direction indicates where the wind is blowing from.
        def compute_track_and_gs(hdg, tas, wind_direction, wind_speed):
            tas_lat = math.cos(deg_to_rad(hdg)) * tas  # lateral component of tas
            tas_lon = math.sin(deg_to_rad(hdg)) * tas  # longitudinal component os tas

            ws_lat = -math.cos(deg_to_rad(wind_direction)) * wind_speed  # lateral component of wind
            ws_lon = -math.sin(deg_to_rad(wind_direction)) * wind_speed  # longitudinal component of wind
            #        ^ these minuses account for the convention to indicate where the wind is blowing FROM, not TO

            gs_lat = tas_lat + ws_lat  # add both cartesian aircraft- and wind vector together...
            gs_lon = tas_lon + ws_lon  # ... to obtain ground speed vector (gs_vec = tas_vec + ws_vec)

            track = rad_to_deg(math.atan2(gs_lon, gs_lat))  # compute direction the ground speed vector points in
            if track < 0:  # atan2 gives result in [-180 degrees, +180 degrees]; correct for that by adding 360 degrees to all negative results
                track += 360

            gs = math.sqrt(
                gs_lat ** 2 + gs_lon ** 2)  # use some pythagoras to compute length of vector ( = ground speed)

            return track, gs


        # compute heading[degrees] and true airspeed[kt] from track[degrees], ground speed[kt], wind direction[degrees] and wind speed[kt]
        # Two-dimensional. Wind direction indicates where the wind is blowing from.
        def compute_tas_and_hdg(track, gs, wind_direction, wind_speed):
            # same logic and formulae as before
            gs_lat = math.cos(deg_to_rad(track)) * gs
            gs_lon = math.sin(deg_to_rad(track)) * gs

            ws_lat = -math.cos(deg_to_rad(wind_direction)) * wind_speed
            ws_lon = -math.sin(deg_to_rad(wind_direction)) * wind_speed

            tas_lat = gs_lat - ws_lat  # tas_vec = gs_vec - ws_vec
            tas_lon = gs_lon - ws_lon

            hdg = rad_to_deg(math.atan2(tas_lon, tas_lat))
            if hdg < 0:
                hdg += 360

            tas = math.sqrt(tas_lat ** 2 + tas_lon ** 2)

            return hdg, tas


        # From here, it's just user interaction
        user_input = ""
        while user_input != "q":
            if user_input == "1":
                tas = float(input("Wie gross ist die True Airspeed? (Eingabe in kt) > "))
                ws = float(input("Wie stark weht der Wind? (Eingabe in kt; positiver Wert bedeutet Rueckenwind, negativer Wert bedeutet Gegenwind) > "))
                print("")
                gs = compute_gs(tas, ws)
                print("Die Ground Speed betraegt", gs, "kt")
            if user_input == "2":
                hdg = float(input("Wie lautet das Heading? (Eingabe in Grad) > "))
                tas = float(input("Wie gross ist die True Airspeed? (Eingabe in kt) > "))
                wind_direction = float(input("Aus welcher Richtung kommt der Wind? (Eingabe in Grad) > "))
                wind_speed = float(input("Wie stark weht der Wind? (Eingabe in kt) > "))
                print("")
                track, gs = compute_track_and_gs(hdg, tas, wind_direction, wind_speed)
                print("Der Track betraegt", round(track), "Grad, bei einer Ground Speed von", round(gs, 2), "kt.")
            if user_input == "3":
                gs = float(input("Wie gross ist die Ground Speed? (Eingabe in kt) > "))
                ws = float(input("Wie stark weht der Wind? (Eingabe in kt; positiver Wert bedeutet Rueckenwind, negativer Wert bedeutet Gegenwind) > "))
                print("")
                tas = compute_tas(gs, ws)
                print("Die True Airspeed betraegt", tas, "kt")
            if user_input == "4":
                track = float(input("Wie lautet der Track? (Eingabe in Grad) > "))
                gs = float(input("Wie gross ist die Ground speed? (Eingabe in kt) > "))
                wind_direction = float(input("Aus welcher Richtung kommt der Wind? (Eingabe in Grad) > "))
                wind_speed = float(input("Wie stark weht der Wind? (Eingabe in kt) > "))
                print("")
                hdg, tas = compute_tas_and_hdg(track, gs, wind_direction, wind_speed)
                print("Das Heading betraegt", round(hdg), "Grad, bei einer True Airspeed von", round(tas, 2), "kt")
            print("")
            print("Aktion waehlen:")
            print("[1] Eindimensionale Umrechnung von TAS in GS")
            print("[2] Zweidimensionale Umrechnung von Heading und TAS in Track und GS")
            print("[3] Eindimensionale Umrechnung von GS in TAS")
            print("[4] Zweidimensionale Umrechnung von Track und GS in Heading und TAS")
            print("[q] beenden")
            print("")
            user_input = str(input("> "))
            print("")
    print("")
    print("Aufgabe waehlen:")
    print("[1] Aufgabe 1 (ISA)")
    print("[2] Aufgabe 2 (TAS <--> GS)")
    print("[q] beenden")
    print("")
    user_input = str(input("> "))
    print("")