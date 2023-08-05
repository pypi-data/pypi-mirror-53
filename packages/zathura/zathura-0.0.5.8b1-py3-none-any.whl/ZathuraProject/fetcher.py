from datetime import datetime

from peewee import ModelSelect

from ZathuraProject.sqlite_definition import (DebugLog, ErrorLog, close_db,
                                              database_connection,
                                              database_start)
from ZathuraProject.utility import Utility


class Fetcher():
    """
    This class will send all the data from the sqlite database
    """
    empty_result = {'error': True}

    def __error_obj_to_dict(self, error_log_object: ErrorLog):
        """
        # generates and returns a dictionary from ErrorLog object
        error_log_object: ErrorLog a ErrorLog object
        """
        return {
            Utility.Tag_User: error_log_object.user,
            Utility.Tag_Error_Name: error_log_object.error_name,
            Utility.Tag_Error_Description: error_log_object.error_description,
            Utility.Tag_Origin: error_log_object.point_of_origin,
            Utility.Tag_Logged_At: Utility.milli_to_datetime(error_log_object.logged_at),
            Utility.Tag_Logged_At_Unix: error_log_object.logged_at,
            Utility.Tag_Is_Resolved: Utility.Tag_Text_Resolved if error_log_object.is_resolved else Utility.Tag_Text_Not_Resolved,
            Utility.Tag_Resolved_At: error_log_object.resolved_at if error_log_object.resolved_at is None else Utility.milli_to_datetime(error_log_object.resolved_at),
            Utility.Tag_Resolved_At_Unix: error_log_object.resolved_at,
            Utility.Tag_Warning_Level: self.__get_warning_level_in_text(error_log_object.warning_level),
        }

    @staticmethod
    def __debug_obj_to_dict(debug_log_object: DebugLog):
        """
        # generates & returns a dictionary from a DebugLog object.
        debug_log_object: DebugLog a DebugLog object
        """
        return {
            Utility.Tag_User: debug_log_object.user,
            Utility.Tag_Message: debug_log_object.message_data,
            Utility.Tag_Origin: debug_log_object.point_of_origin,
            Utility.Tag_Logged_At: Utility.milli_to_datetime(debug_log_object.logged_at),
            Utility.Tag_Logged_At_Unix: debug_log_object.logged_at,
        }

    def __generate_error_return_payload(self, log_payload: ModelSelect):
        """
        # generates error payload for return
        """
        all_error_logs = list()
        for err in log_payload:
            all_error_logs.append(self.__error_obj_to_dict(err))
        return {Utility.Tag_Total: len(all_error_logs), Utility.Tag_Log: all_error_logs}

    @staticmethod
    def __get_warning_level_in_text(warning_level: int):
        _ = {
            '0': 'NOTSET',
            '1': 'DEBUG',
            '2': 'INFO',
            '3': 'WARNING',
            '4': 'ERROR',
            '5': 'CRITICAL'
        }
        return _[str(warning_level)]

    def __generate_verbose_return_payload(self, debug_payload: ModelSelect):
        """
        # generates debug payload for return
        """
        all_logs = list()
        for log in debug_payload:
            all_logs.append(self.__debug_obj_to_dict(log))
        return {Utility.Tag_Total: len(all_logs), Utility.Tag_Log: all_logs}

    def get_all_error_log(self, show_all: bool = False, desc: bool = False):
        """
        # returns all error_log table data on a list which are not resolved yet
        show_all: bool filters out the is_resolved = True value if show_all is False
        """
        database_connection()  # initiate database connection before doing anything.
        if show_all:
            if desc:
                err_logs = ErrorLog.select().order_by(ErrorLog.logged_at.desc())
            else:
                err_logs = ErrorLog.select()
        else:
            if desc:
                err_logs = ErrorLog.select().where(ErrorLog.is_resolved !=
                                                   True).order_by(ErrorLog.logged_at.desc())
            else:
                err_logs = ErrorLog.select().where(ErrorLog.is_resolved != True)
        close_db()
        return self.__generate_error_return_payload(err_logs)

    def get_all_debug_log(self):
        """
        # returns all debug_log table data on a list
        """
        database_connection()  # initiate database connection before doing anything.
        debug_logs = DebugLog.select()
        close_db()
        return self.__generate_verbose_return_payload(debug_logs)

    def get_error_by_user(self, user: str, limit: int = 0, desc: bool = False, first_limit: datetime = None, last_limit: datetime = None):
        """
        # returns error generated for a user. datetime is not both inclusive, exclude the last date.
        # username is mandatory in this case.
        # ascending order is by default otherwise.
        # ordering is when the error is logged.
        user: str error report generated under a particular user
        limit: int limits the number of error searchable
        desc: bool whether to show the result in ascending or descending order
        first_limit: datetime shows result after this limit
        last_limit: shows result before this limit (exclusive)
        """
        if len(user) == 0:
            result = self.empty_result
            result[Utility.Tag_error_message] = "Username cannot be empty for this function!"
            return result
        user = user.strip()
        # initiate database connection before doing anything.
        database_connection()
        if first_limit is None and last_limit is None:
            if limit != 0:
                if desc:
                    # descending order with limit
                    errors = ErrorLog.select().where(ErrorLog.user == user).order_by(
                        ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # ascending order with limit
                    errors = ErrorLog.select().where(ErrorLog.user == user).limit(limit)
            else:
                if desc:
                    # descending order without limit
                    errors = ErrorLog.select().where(
                        ErrorLog.user == user).order_by(ErrorLog.logged_at.desc())
                else:
                    # ascending order without limit
                    errors = ErrorLog.select().where(ErrorLog.user == user)
        else:
            # filter by datetime. and same limit order
            first_limit = Utility.unix_time_millis(first_limit)
            if last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)
            param_user = (ErrorLog.user == user)
            param_date_filter_one = (ErrorLog.logged_at >= first_limit)
            param_date_filter_two = (ErrorLog.logged_at <= last_limit)
            if limit != 0:
                if desc:
                    # descending order with limit date filter included
                    errors = ErrorLog.select().where(param_user & param_date_filter_one &
                                                     param_date_filter_two).order_by(ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # ascending order without limit date filter included
                    errors = ErrorLog.select().where(param_user & param_date_filter_one &
                                                     param_date_filter_two).limit(limit)
            else:
                if desc:
                    # descending order without limit date filter included
                    errors = ErrorLog.select().where(param_user & param_date_filter_one &
                                                     param_date_filter_two).order_by(ErrorLog.logged_at.desc())
                else:
                    # ascending order without limit date filter included
                    errors = ErrorLog.select().where(
                        param_user & param_date_filter_one & param_date_filter_two)
        close_db()
        return self.__generate_error_return_payload(errors)

    def get_error_by_date_limit(self, beginning_limit: datetime, ending_limit: datetime = None, limit: int = 0, desc: bool = False):
        """
        # get reports under a date limit from all users
        beginning_limit: datetime starting time, inclusive
        ending_limit: datetime ending time, exclusive
        limit: int limits the number of search result.
        desc: bool whether to show the result in descending order
        """
        if beginning_limit is None:
            result = self.empty_result
            result[Utility.Tag_error_message] = "Please insert the first date to search after a specific time."
            return result
        first_limit = Utility.unix_time_millis(beginning_limit)
        if ending_limit is None:
            last_limit = Utility.current_time_in_milli()
        else:
            last_limit = Utility.unix_time_millis(ending_limit)
        # initiate database connection before doing anything.
        database_connection()
        param_filter_one = (ErrorLog.logged_at >= first_limit)
        param_filter_two = (ErrorLog.logged_at <= last_limit)

        if limit != 0:
            if desc:
                # search under a limit in descending order
                errors = ErrorLog.select().where(param_filter_one & param_filter_two).order_by(
                    ErrorLog.logged_at.desc()).limit(limit)
            else:
                # search under a limit in ascending order
                errors = ErrorLog.select().where(param_filter_one & param_filter_two).limit(limit)
        else:
            if desc:
                # search without limit in descending order
                errors = ErrorLog.select().where(
                    param_filter_one & param_filter_two).order_by(ErrorLog.logged_at.desc())
            else:
                # search without limit in ascending order
                errors = ErrorLog.select().where(param_filter_one & param_filter_two)
        close_db()
        return self.__generate_error_return_payload(errors)

    # def search by error_name
    def get_error_by_error_name(self, error_name: str, first_limit: datetime = None, last_limit: datetime = None, limit: int = 0, desc: bool = False):
        """
        # searches errors by error name. filters will be applied based on parameter
        error_name: what's the name of error you want to search under.
        first_limit: first date limit to be applied
        last_limit: last date limit to be applied, not inclusive
        limit: limits the number of data on search result.
        desc: sort the result in descending order or ascending order. (By default, ascending order)
        """
        if error_name is None or len(error_name) == 0:
            result = self.empty_result
            result[Utility.Tag_error_message] = "Error name cannot be empty on this search"
            return result
        error_name = error_name.strip()
        error_name = error_name.lower()
        # initiate database connection before doing anything.
        database_connection()
        if first_limit is None and last_limit is None:
            if limit != 0:
                if desc:
                    # search with limit in descending order under no date limit
                    errors = ErrorLog.select().where(ErrorLog.error_name == error_name).order_by(
                        ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # search with limit in ascending order under no date limit
                    errors = ErrorLog.select().where(ErrorLog.error_name == error_name).limit(limit)
            else:
                if desc:
                    # search without limit in descending order under no date limit
                    errors = ErrorLog.select().where(ErrorLog.error_name ==
                                                     error_name).order_by(ErrorLog.logged_at.desc())
                else:
                    # search without limit in ascending order under no date limit
                    errors = ErrorLog.select().where(ErrorLog.error_name == error_name)
        else:
            # filter under date limit
            if first_limit is not None:
                first_limit = Utility.unix_time_millis(first_limit)
            else:
                first_limit = Utility.current_time_in_milli()
            if last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)

            param_filter_one = (ErrorLog.error_name == error_name)
            param_filter_two = (ErrorLog.logged_at >= first_limit)
            param_filter_three = (ErrorLog.logged_at <= last_limit)

            if limit != 0:
                if desc:
                    # search with limit in descending order under date limit
                    errors = ErrorLog.select().where(param_filter_one & param_filter_two &
                                                     param_filter_three).order_by(ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # search with limit in ascending order under date limit
                    errors = ErrorLog.select().where(param_filter_one & param_filter_two &
                                                     param_filter_three).limit(limit)
            else:
                if desc:
                    # search without limit in descending order under date limit
                    errors = ErrorLog.select().where(param_filter_one & param_filter_two &
                                                     param_filter_three).order_by(ErrorLog.logged_at.desc())
                else:
                    # search without limit in ascending order under date limit
                    errors = ErrorLog.select().where(
                        param_filter_one & param_filter_two & param_filter_three)
        close_db()
        return self.__generate_error_return_payload(errors)

    def get_error_by_origin(self, origin: str, first_limit: datetime = None, last_limit: datetime = None, limit: int = 0, desc: bool = False):
        """
        # searches error by point of origin, where the error is originated when the error is logged.
        # But you better catch the error with an except block. and manually register it. 
        origin: str name of the function or class
        first_limit: datetime first date limit for filtering purpose
        last_limit: datetime last date limit to filter out 
        limit: int limits the amount of returned result.
        desc: bool filter the data in descending order (Ascending is by default)
        """
        if origin is not None or len(origin) != 0:
            # Point of origin can be None.
            origin = origin.strip()
            origin = origin.lower()
        # initiate database connection before doing anything.
        database_connection()
        if first_limit is None and last_limit is None:
            if limit != 0:
                # search with limit and no date limit applied
                if desc:
                    # show result in descending order with limit but no date filter
                    errors = ErrorLog.select().where(ErrorLog.point_of_origin == origin).order_by(
                        ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # show result in ascending order with limit but no date filter
                    errors = ErrorLog.select().where(ErrorLog.point_of_origin == origin).limit(limit)
            else:
                if desc:
                    # show result in descending order without limit but no date filter
                    errors = ErrorLog.select().where(ErrorLog.point_of_origin ==
                                                     origin).order_by(ErrorLog.logged_at.desc())
                else:
                    # show result in ascending order without but no date filter
                    errors = ErrorLog.select().where(ErrorLog.point_of_origin == origin)
        else:
            first_limit = Utility.unix_time_millis(first_limit)
            if last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)
            filter_param_one = (ErrorLog.point_of_origin == origin)
            filter_param_two = (ErrorLog.logged_at >= first_limit)
            filter_param_three = (ErrorLog.logged_at <= last_limit)

            if limit != 0:
                # search with limit and no date limit applied
                if desc:
                    # show result in descending order with limit WITH date filter
                    errors = ErrorLog.select().where(filter_param_one & filter_param_two &
                                                     filter_param_three).order_by(ErrorLog.logged_at.desc()).limit(limit)
                else:
                    # show result in ascending order with limit WITH date filter
                    errors = ErrorLog.select().where(filter_param_one & filter_param_two &
                                                     filter_param_three).limit(limit)
            else:
                if desc:
                    # show result in descending order without limit WITH date filter
                    errors = ErrorLog.select().where(filter_param_one & filter_param_two &
                                                     filter_param_three).order_by(ErrorLog.logged_at.desc())
                else:
                    # show result in ascending order without WITH date filter
                    errors = ErrorLog.select().where(
                        filter_param_one & filter_param_two & filter_param_three)
        close_db()
        return self.__generate_error_return_payload(errors)

    def get_debug_by_origin(self, origin: str = '', first_limit: datetime = None, last_limit: datetime = None):
        """
        # returns all debug data filters by origin; if needed.
        first_limit: datetime filters out data before this limit
        last_limit: datetime filters out data after this limit
        origin: str point of origin of any debug msg that needs to be on this list.
        """
        if origin is not None and len(origin) > 0:
            origin = origin.strip()
            origin = origin.lower()
        else:
            return self.get_all_debug_log()  # blind send everything.

        # initiate database connection before doing anything.
        database_connection()
        filter_param_one = (DebugLog.point_of_origin == origin)

        if first_limit is None and last_limit is None:
            debugs = DebugLog.select().where(filter_param_one)
        else:
            first_limit = Utility.unix_time_millis(first_limit)
            if last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)
            filter_param_two = (DebugLog.logged_at >= first_limit)
            filter_param_three = (DebugLog.logged_at <= last_limit)
            debugs = DebugLog.select().where(
                filter_param_one & filter_param_two & filter_param_three)
        close_db()
        return self.__generate_verbose_return_payload(debugs)

    def get_debug_by_developers(self, developers_name: str = '', first_limit: datetime = None, last_limit: datetime = None):
        """
        # returns all debug data filters by developers; if needed.
        first_limit: datetime filters out data before this limit
        last_limit: datetime filters out data after this limit
        developers_name: str developers_name : who wrote the debug message. For debugging person. Could be None or empty string.
        """
        if len(developers_name) == 0 or developers_name is None:
            return self.get_all_debug_log()
        # initiate database connection before doing anything.
        database_connection()
        if first_limit is None and last_limit is None:
            debugs = DebugLog.select().where(DebugLog.user == developers_name)
        else:
            first_limit = Utility.unix_time_millis(first_limit)
            if last_limit is None:
                last_limit = Utility.current_time_in_milli()
            else:
                last_limit = Utility.unix_time_millis(last_limit)
            debugs = DebugLog.select().where((DebugLog.user == developers_name) & (
                DebugLog.logged_at >= first_limit) & (DebugLog.logged_at <= last_limit))
        close_db()
        return self.__generate_verbose_return_payload(debugs)

    def mark_resolve(self, error_name: str, origin: str):
        """
        # Mark resolved some errors
        error_name: str the error name u want to mark as resolved.
        origin: str point of origin of this particular error.
        they are both necessary
        """
        result = self.empty_result
        if error_name is None or len(error_name) == 0:
            result[Utility.Tag_error_message] = "missing error name!"
            return result
        if origin is None or len(origin) == 0:
            result[Utility.Tag_error_message] = 'missing error origin!'
            return result
        # initiate database connection before doing anything.
        database_connection()
        error_name = error_name.strip().lower()
        origin = origin.strip().lower()
        filter_one = (ErrorLog.error_name == error_name)
        filter_two = (ErrorLog.point_of_origin == origin)
        filter_three = (ErrorLog.is_resolved != True)
        query = (ErrorLog.update({ErrorLog.is_resolved: True, ErrorLog.resolved_at: Utility.current_time_in_milli()}).where(
            filter_one & filter_two & filter_three))
        result = query.execute()
        close_db()
        return result

    def delete_old_debug(self):
        from datetime import timedelta
        # initiate database connection before doing anything.
        database_connection()
        limit = (datetime.now() - timedelta(days=7)).replace(hour=0,
                                                             minute=0, second=0, microsecond=0)
        today = Utility.unix_time_millis(limit)
        delete_stuff = DebugLog.delete().where(DebugLog.logged_at < today)
        _ = delete_stuff.execute()
        close_db()
