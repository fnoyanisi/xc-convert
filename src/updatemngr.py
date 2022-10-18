""""
Manages the checks for the updates
"""
import urllib.request
from urllib.error import URLError
from tkinter import messagebox
from socket import timeout


class UpdateManager:
    def __init__(self):
        self.updateUrl = "https://raw.githubusercontent.com/fnoyanisi/xc-convert/master/VERSION"
        self.downloadUrl = "https://github.com/fnoyanisi/xc-convert/archive/refs/heads/master.zip"
        self.version = ""

    # v -   the local version
    # s -   silent mode
    # if the silent mode is used, the application does not prompt the user
    # when no update is needed
    def check_for_updates(self, v, s):
        local_version = v
        silent_mode = s

        # read the online version info
        try:
            response = urllib.request.urlopen(self.updateUrl, timeout=1)
        except NameError:
            messagebox.showerror("Update Manager Network Error", "Cannot open the update URL")
            return
        except URLError as e:
            messagebox.showerror("Update Manager URL Error", str(e.reason))
            return
        except timeout:
            messagebox.showerror("Update Manager Network Error", "Request timeout")
            return

        data = response.read()
        online_version = data.decode('utf-8')

        # compare the version information
        # do nothing if the current version is
        cmp = self.__compare_version_info(online_version, local_version)
        if cmp == -1:
            messagebox.showerror("Wrong version information",
                                 "Please make sure your version information is correct : " + str(local_version))
        elif cmp == 1:
            msg1 = "A new version of xc-convert is available. Please download it from " + self.downloadUrl
            msg2 = "Current version: " + str(local_version)
            msg3 = "Online version: " + str(online_version)
            messagebox.showinfo("A New Version is Available", msg1 + "\n\n" + msg2 + "\n" + msg3)
        elif cmp == 0 and not silent_mode:
            messagebox.showinfo("You are up to date", "There is no updates for version " + str(local_version))

    # compares two version information of the form
    # Major.Minor.Patch
    #
    # e.g.
    # 0.6.4 vs 7.0.1
    @staticmethod
    def __compare_version_info(v1, v2):
        arr_v1 = v1.split(".")
        arr_v2 = v2.split(".")

        # make sure we have major.minor.patch
        # in case patch is missing, assume "0"
        # in any case, we expect minor to be present
        len_v1 = len(arr_v1)
        len_v2 = len(arr_v2)

        if len_v1 < 2 or len_v2 < 2:
            msg = "v1 : " + v1 + ", v2 : " + v2
            messagebox.showerror("Unsupported version number format", msg)
            return

        if len_v1 == 2:
            arr_v1.append("0")

        if len_v2 == 2:
            arr_v2.append("0")

        # converts to integer from string
        arr_v1 = [int(i) for i in arr_v1]
        arr_v2 = [int(i) for i in arr_v2]

        # returns 1 if version 1 is bigger and -1 if
        # version 2 is bigger and 0 if equal
        for i in range(len(arr_v1)):
            if arr_v1[i] > arr_v2[i]:
                return 1
            elif arr_v2[i] > arr_v1[i]:
                return -1
        return 0