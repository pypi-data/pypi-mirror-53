﻿import sys
import time
import re
import progressbar
import threading
# import requests
# from requests.packages.urllib3.exceptions import InsecureRequestWarning
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

try:
    import DataType
    import Config
    import Util
    import i18n
    import ConnectCore
    import Log
    import Screens
    import Exceptions
    import Command
except ModuleNotFoundError:
    from . import DataType
    from . import Config
    from . import Util
    from . import i18n
    from . import ConnectCore
    from . import Log
    from . import Screens
    from . import Exceptions
    from . import Command


Version = Config.Version

Language = i18n.Language
ConnectMode = ConnectCore.ConnectMode
LogLevel = Log.Level
Command = Command
PushType = DataType.PushType
PostSearchType = DataType.PostSearchType
IndexType = DataType.IndexType
WaterBallOperateType = DataType.WaterBallOperateType
WaterBallType = DataType.WaterBallType
CallStatus = DataType.CallStatus
PostDeleteStatus = DataType.PostDeleteStatus


class Library(object):
    def __init__(
        self,
        Language: int = 0,
        ConnectMode: int = 0,
        LogLevel: int = 0,
        ScreenTimeOut: int = 0,
        ScreenLongTimeOut: int = 0,
        LogHandler=None,
    ):

        if LogHandler is not None:
            hasLogHandler = True
            setLogHandlerResult = True
            try:
                LogHandler(f'PTT Library v {Version}')
                LogHandler('Developed by PTT CodingMan')
            except:
                LogHandler = None
                setLogHandlerResult = False
        else:
            hasLogHandler = False

        print(f'PTT Library v {Version}')
        print('Developed by PTT CodingMan')

        self._LoginStatus = False

        Config.load()

        if not isinstance(Language, int):
            raise TypeError('Language must be integer')
        if not isinstance(ConnectMode, int):
            raise TypeError('ConnectMode must be integer')
        if not isinstance(LogLevel, int):
            raise TypeError('LogLevel must be integer')
        if not isinstance(ScreenTimeOut, int):
            raise TypeError('ScreenTimeOut must be integer')
        if not isinstance(ScreenLongTimeOut, int):
            raise TypeError('ScreenLongTimeOut must be integer')

        if ScreenTimeOut != 0:
            Config.ScreenTimeOut = ScreenTimeOut
        if ScreenLongTimeOut != 0:
            Config.ScreenLongTimeOut = ScreenLongTimeOut

        if LogLevel == 0:
            LogLevel = Config.LogLevel
        elif not Util.checkRange(Log.Level, LogLevel):
            raise ValueError('Unknow LogLevel', LogLevel)
        else:
            Config.LogLevel = LogLevel

        if Language == 0:
            Language = Config.Language
        elif not Util.checkRange(i18n.Language, Language):
            raise ValueError('Unknow language', Language)
        else:
            Config.Language = Language
        i18n.load(Language)

        if LogHandler is not None:
            Log.Handler = LogHandler
            Log.showValue(
                Log.Level.INFO,
                i18n.LogHandler,
                i18n.Init
            )
        elif hasLogHandler and not setLogHandlerResult:
            Log.showValue(
                Log.Level.INFO,
                i18n.LogHandler,
                [
                    i18n.Init,
                    i18n.Fail
                ]
            )

        if Language == i18n.Language.Chinese:
            Log.showValue(Log.Level.INFO, [
                i18n.ChineseTranditional,
                i18n.LanguageModule
            ],
                i18n.Init
            )
        elif Language == i18n.Language.English:
            Log.showValue(Log.Level.INFO, [
                i18n.English,
                i18n.LanguageModule
            ],
                i18n.Init
            )

        if ConnectMode == 0:
            ConnectMode = Config.ConnectMode
        elif not Util.checkRange(ConnectCore.ConnectMode, ConnectMode):
            raise ValueError('Unknow ConnectMode', ConnectMode)
        else:
            Config.ConnectMode = ConnectMode
        self._ConnectCore = ConnectCore.API(ConnectMode)
        self._ExistBoardList = []
        self._LastThroWaterBallTime = 0
        self._ThreadID = threading.get_ident()

        Log.showValue(
            Log.Level.DEBUG,
            'ThreadID',
            self._ThreadID
        )

        Log.showValue(
            Log.Level.INFO, [
                i18n.PTT,
                i18n.Library,
                ' v ' + Version,
            ],
            i18n.Init
        )

    def _OneThread(self):
        CurrentThreadID = threading.get_ident()
        if CurrentThreadID == self._ThreadID:
            return
        Log.showValue(
            Log.Level.DEBUG,
            'ThreadID',
            self._ThreadID
        )
        Log.showValue(
            Log.Level.DEBUG,
            'Current thread id',
            CurrentThreadID
        )
        raise Exceptions.MultiThreadOperated()

    def getVersion(self) -> str:
        self._OneThread()
        return Config.Version

    def _login(
        self,
        ID: str,
        Password: str,
        KickOtherLogin: bool = False
    ):

        if self._LoginStatus:
            self.logout()

        if not isinstance(ID, str):
            raise TypeError(Log.merge([
                i18n.ID,
                i18n.MustBe,
                i18n.String
            ]))
        if not isinstance(Password, str):
            raise TypeError(Log.merge([
                i18n.Password,
                i18n.MustBe,
                i18n.String
            ]))
        if not isinstance(KickOtherLogin, bool):
            raise TypeError(Log.merge([
                'KickOtherLogin',
                i18n.MustBe,
                i18n.Boolean
            ]))

        Config.KickOtherLogin = KickOtherLogin

        def KickOtherLoginDisplayMsg():
            if Config.KickOtherLogin:
                return i18n.KickOtherLogin
            return i18n.NotKickOtherLogin

        def KickOtherLoginResponse(Screen):
            if Config.KickOtherLogin:
                return 'y' + Command.Enter
            return 'n' + Command.Enter

        if len(Password) > 8:
            Password = Password[:8]

        ID = ID.strip()
        Password = Password.strip()

        self._ID = ID
        self._Password = Password

        Log.showValue(
            Log.Level.INFO,
            [
                i18n.Login,
                i18n.ID
            ],
            ID
        )

        Config.KickOtherLogin = KickOtherLogin

        self._ConnectCore.connect()

        TargetList = [
            ConnectCore.TargetUnit(
                i18n.HasNewMailGotoMainMenu,
                '你有新信件',
                Response=Command.GoMainMenu,
            ),
            ConnectCore.TargetUnit(
                i18n.LoginSuccess,
                Screens.Target.MainMenu,
                BreakDetect=True
            ),
            ConnectCore.TargetUnit(
                i18n.ErrorIDPW,
                '密碼不對或無此帳號',
                BreakDetect=True,
                Exceptions=Exceptions.WrongIDorPassword()
            ),
            ConnectCore.TargetUnit(
                i18n.LoginTooOften,
                '登入太頻繁',
                BreakDetect=True,
                Exceptions=Exceptions.LoginTooOften()
            ),
            ConnectCore.TargetUnit(
                i18n.SystemBusyTryLater,
                '系統過載',
                BreakDetect=True,
            ),
            ConnectCore.TargetUnit(
                i18n.DelWrongPWRecord,
                '您要刪除以上錯誤嘗試的記錄嗎',
                Response='y' + Command.Enter,
            ),
            ConnectCore.TargetUnit(
                i18n.MailBoxFull,
                '您保存信件數目',
                Response=Command.GoMainMenu,
            ),
            ConnectCore.TargetUnit(
                i18n.PostNotFinish,
                '有一篇文章尚未完成',
                Response='Q' + Command.Enter,
            ),
            ConnectCore.TargetUnit(
                i18n.SigningUnPleaseWait,
                '登入中，請稍候',
            ),
            ConnectCore.TargetUnit(
                KickOtherLoginDisplayMsg,
                '您想刪除其他重複登入的連線嗎',
                Response=KickOtherLoginResponse,
            ),
            ConnectCore.TargetUnit(
                i18n.AnyKeyContinue,
                '任意鍵',
                Response='q',
            ),
            ConnectCore.TargetUnit(
                i18n.SigningUpdate,
                '正在更新與同步線上使用者及好友名單',
            ),
        ]

        CmdList = []
        CmdList.append(ID)
        CmdList.append(Command.Enter)
        CmdList.append(Password)
        CmdList.append(Command.Enter)

        Cmd = ''.join(CmdList)

        index = self._ConnectCore.send(
            Cmd,
            TargetList,
            ScreenTimeout=Config.ScreenLongTimeOut,
            Refresh=False,
            Secret=True
        )
        if index != 1:
            raise Exceptions.LoginError()

        OriScreen = self._ConnectCore.getScreenQueue()[-1]
        if '> (' in OriScreen:
            self._Cursor = DataType.Cursor.New
            Log.log(
                Log.Level.DEBUG,
                i18n.NewCursor
            )
        else:
            self._Cursor = DataType.Cursor.Old
            Log.log(
                Log.Level.DEBUG,
                i18n.OldCursor
            )

        if self._Cursor not in Screens.Target.InBoardWithCursor:
            Screens.Target.InBoardWithCursor.append(self._Cursor)

        self._UnregisteredUser = False
        if '(T)alk' not in OriScreen:
            self._UnregisteredUser = True
        if '(P)lay' not in OriScreen:
            self._UnregisteredUser = True
        if '(N)amelist' not in OriScreen:
            self._UnregisteredUser = True

        if self._UnregisteredUser:
            Log.log(
                Log.Level.INFO,
                i18n.UnregisteredUserCantUseAllAPI
            )

        self._LoginStatus = True

    def login(
        self,
        ID: str,
        Password: str,
        KickOtherLogin: bool = False
    ):
        self._OneThread()
        try:
            return self._login(
                ID,
                Password,
                KickOtherLogin=KickOtherLogin
            )
        except Exceptions.LoginError:
            return self._login(
                ID,
                Password,
                KickOtherLogin=KickOtherLogin
            )

    def logout(self):
        self._OneThread()

        if not self._LoginStatus:
            return

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('g')
        CmdList.append(Command.Enter)
        CmdList.append('y')
        CmdList.append(Command.Enter)
        CmdList.append(Command.Enter)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                [
                    i18n.Logout,
                    i18n.Success,
                ],
                '任意鍵',
                BreakDetect=True,
            ),
        ]

        Log.log(
            Log.Level.INFO,
            [
                i18n.Start,
                i18n.Logout
            ]
        )

        try:
            self._ConnectCore.send(Cmd, TargetList)
            self._ConnectCore.close()
        except Exceptions.ConnectionClosed:
            pass
        except RuntimeError:
            pass

        self._LoginStatus = False

        Log.showValue(
            Log.Level.INFO,
            i18n.Logout,
            i18n.Done
        )

    def log(self, Msg):
        self._OneThread()
        Log.log(Log.Level.INFO, Msg)

    def getTime(self) -> str:
        self._OneThread()
        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('A')
        CmdList.append(Command.Right)
        CmdList.append(Command.Left)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                [
                    i18n.GetPTTTime,
                    i18n.Success,
                ],
                Screens.Target.MainMenu,
                BreakDetect=True
            ),
        ]

        index = self._ConnectCore.send(Cmd, TargetList)
        if index != 0:
            return None

        OriScreen = self._ConnectCore.getScreenQueue()[-1]

        pattern = re.compile('[\d]+:[\d][\d]')
        Result = pattern.search(OriScreen)

        if Result is not None:
            return Result.group(0)
        return None

    def getPost(
        self,
        Board: str,
        PostAID: str = None,
        PostIndex: int = 0,
        SearchType: int = 0,
        SearchCondition: str = None,
        Query: bool = False
    ):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if not isinstance(Board, str):
            raise TypeError(Log.merge([
                'Board',
                i18n.MustBe,
                i18n.String
            ]))
        if not isinstance(PostAID, str) and PostAID is not None:
            raise TypeError(Log.merge([
                'PostAID',
                i18n.MustBe,
                i18n.String
            ]))
        if not isinstance(PostIndex, int):
            raise TypeError(Log.merge([
                'PostIndex',
                i18n.MustBe,
                i18n.Integer
            ]))

        if not isinstance(SearchType, int):
            raise TypeError(Log.merge([
                'SearchType',
                i18n.MustBe,
                i18n.Integer
            ]))
        if (not isinstance(SearchCondition, str) and
                SearchCondition is not None):
            raise TypeError(Log.merge([
                'SearchCondition',
                i18n.MustBe,
                i18n.String
            ]))

        if len(Board) == 0:
            raise ValueError(Log.merge([
                i18n.Board,
                i18n.ErrorParameter,
                Board
            ]))

        if PostIndex != 0 and isinstance(PostAID, str):
            raise ValueError(Log.merge([
                'PostIndex',
                'PostAID',
                i18n.ErrorParameter,
                i18n.BothInput
            ]))

        if PostIndex == 0 and PostAID is None:
            raise ValueError(Log.merge([
                'PostIndex',
                'PostAID',
                i18n.ErrorParameter
            ]))

        if (SearchType != 0 and
                not Util.checkRange(DataType.PostSearchType, SearchType)):
            raise ValueError(Log.merge([
                'SearchType',
                i18n.ErrorParameter,
            ]))

        if SearchCondition is not None and SearchType == 0:
            raise ValueError(Log.merge([
                'SearchType',
                i18n.ErrorParameter,
            ]))

        if SearchType == DataType.PostSearchType.Push:
            try:
                S = int(SearchCondition)
            except ValueError:
                raise ValueError(Log.merge([
                    'SearchCondition',
                    i18n.ErrorParameter,
                ]))

            if not (-100 <= S <= 110):
                raise ValueError(Log.merge([
                    'SearchCondition',
                    i18n.ErrorParameter,
                ]))

        if PostAID is not None and SearchCondition is not None:
            raise ValueError(Log.merge([
                'PostAID',
                'SearchCondition',
                i18n.ErrorParameter,
                i18n.BothInput,
            ]))

        if PostIndex > 0:
            NewestIndex = self._getNewestIndex(
                DataType.IndexType.Board,
                Board=Board,
                SearchType=SearchType,
                SearchCondition=SearchCondition
            )

            if PostIndex > NewestIndex:
                raise ValueError(Log.merge([
                    'PostIndex',
                    i18n.ErrorParameter,
                    i18n.OutOfRange,
                ]))
        for i in range(2):

            NeedContinue = False
            Post = None
            try:
                Post = self._getPost(
                    Board,
                    PostAID,
                    PostIndex,
                    SearchType,
                    SearchCondition,
                    Query
                )
            except Exceptions.ParseError as e:
                if i == 1:
                    raise e
                NeedContinue = True
            except Exceptions.UnknowError as e:
                if i == 1:
                    raise e
                NeedContinue = True
            except Exceptions.NoSuchBoard as e:
                if i == 1:
                    raise e
                NeedContinue = True
            except ConnectCore.NoMatchTargetError as e:
                if i == 1:
                    raise e
                NeedContinue = True

            if Post is None:
                NeedContinue = True
            elif not Post.isFormatCheck():
                NeedContinue = True

            if NeedContinue:
                Log.log(
                    Log.Level.DEBUG,
                    'Wait for retry repost'
                )
                time.sleep(0.1)
                continue

            break
        return Post

    def _getPost(
        self,
        Board: str,
        PostAID: str = None,
        PostIndex: int = 0,
        SearchType: int = 0,
        SearchCondition: str = None,
        Query: bool = False,
    ):

        if Board.lower() not in self._ExistBoardList:
            CmdList = []
            CmdList.append(Command.GoMainMenu)
            CmdList.append('qs')
            CmdList.append(Board)
            CmdList.append(Command.Enter)
            CmdList.append(Command.Ctrl_C * 2)
            CmdList.append(Command.Space)
            CmdList.append('i')
            Cmd = ''.join(CmdList)

            TargetList = [
                ConnectCore.TargetUnit(
                    i18n.AnyKeyContinue,
                    '任意鍵繼續',
                    BreakDetect=True,
                    LogLevel=Log.Level.DEBUG
                )
            ]

            index = self._ConnectCore.send(Cmd, TargetList)
            OriScreen = self._ConnectCore.getScreenQueue()[-1]
            if index < 0:
                raise Exceptions.UnknowError(OriScreen)

            BoardNameLine = [line.strip() for line in OriScreen.split(
                '\n') if line.strip().startswith('《')]
            if len(BoardNameLine) != 1:
                raise Exceptions.UnknowError(OriScreen)
            BoardNameLine = BoardNameLine[0]
            if '《' not in BoardNameLine or '》' not in BoardNameLine:
                raise Exceptions.UnknowError(BoardNameLine)

            BoardName = BoardNameLine[1:BoardNameLine.find('》')]

            Log.showValue(
                Log.Level.DEBUG,
                'Find Board Name',
                BoardName
            )
            self._ExistBoardList.append(BoardName.lower())

            if BoardName.lower() != Board.lower():
                raise Exceptions.NoSuchBoard(Board)

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('qs')
        CmdList.append(Board)
        CmdList.append(Command.Enter)
        CmdList.append(Command.Ctrl_C * 2)
        CmdList.append(Command.Space)

        if PostAID is not None:
            CmdList.append('#' + PostAID)

        elif PostIndex != 0:
            if SearchCondition is not None:
                if SearchType == DataType.PostSearchType.Keyword:
                    CmdList.append('/')
                elif SearchType == DataType.PostSearchType.Author:
                    CmdList.append('a')
                elif SearchType == DataType.PostSearchType.Push:
                    CmdList.append('Z')
                elif SearchType == DataType.PostSearchType.Mark:
                    CmdList.append('G')
                elif SearchType == DataType.PostSearchType.Money:
                    CmdList.append('A')

                CmdList.append(SearchCondition)
                CmdList.append(Command.Enter)

            CmdList.append(str(PostIndex))

        CmdList.append(Command.Enter)
        CmdList.append(Command.QueryPost)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                [
                    i18n.CatchPost,
                    i18n.Success,
                ],
                Screens.Target.QueryPost,
                BreakDetect=True,
                Refresh=False,
                LogLevel=Log.Level.DEBUG
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.PostDeled,
                    i18n.Success,
                ],
                Screens.Target.InBoard,
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
        ]

        index = self._ConnectCore.send(Cmd, TargetList)
        OriScreen = self._ConnectCore.getScreenQueue()[-1]

        PostAuthor = None
        PostTitle = None
        if index < 0 or index == 1:
            # 文章被刪除
            Log.log(Log.Level.DEBUG, i18n.PostDeled)
            PostDelStatus = 0

            Log.showValue(
                Log.Level.DEBUG,
                'OriScreen',
                OriScreen
            )

            CursorLine = [line for line in OriScreen.split(
                '\n') if line.startswith(self._Cursor)]

            if len(CursorLine) != 1:
                raise Exceptions.UnknowError(OriScreen)

            CursorLine = CursorLine[0]
            Log.showValue(
                Log.Level.DEBUG,
                'CursorLine',
                CursorLine
            )

            pattern = re.compile('[\d]+\/[\d]+')
            PatternResult = pattern.search(CursorLine)
            if PatternResult is None:
                ListDate = None
            else:
                ListDate = PatternResult.group(0)
                ListDate = ListDate[-5:]

            pattern = re.compile('\[[\w]+\]')
            PatternResult = pattern.search(CursorLine)
            if PatternResult is not None:
                PostDelStatus = DataType.PostDeleteStatus.ByAuthor
            else:
                pattern = re.compile('<[\w]+>')
                PatternResult = pattern.search(CursorLine)
                PostDelStatus = DataType.PostDeleteStatus.ByModerator

            # > 79843     9/11 -             □ (本文已被吃掉)<
            # > 76060     8/28 -             □ (本文已被刪除) [weida7332]
            # print(f'O=>{CursorLine}<')
            if PatternResult is not None:
                PostAuthor = PatternResult.group(0)[1:-1]
            else:
                PostAuthor = None
                PostDelStatus = DataType.PostDeleteStatus.ByUnknow

            Log.showValue(Log.Level.DEBUG, 'ListDate', ListDate)
            Log.showValue(Log.Level.DEBUG, 'PostAuthor', PostAuthor)
            Log.showValue(Log.Level.DEBUG, 'PostDelStatus', PostDelStatus)

            return DataType.PostInfo(
                Board=Board,
                Author=PostAuthor,
                ListDate=ListDate,
                DeleteStatus=PostDelStatus,
                FormatCheck=True
            )

        elif index == 0:

            LockPost = False
            CursorLine = [line for line in OriScreen.split(
                '\n') if line.startswith(self._Cursor)][0]
            PostAuthor = CursorLine
            if '□' in PostAuthor:
                PostAuthor = PostAuthor[:PostAuthor.find('□')].strip()
            elif 'R:' in PostAuthor:
                PostAuthor = PostAuthor[:PostAuthor.find('R:')].strip()
            elif ' 轉 ' in PostAuthor:
                PostAuthor = PostAuthor[:PostAuthor.find('轉')].strip()
            elif ' 鎖 ' in PostAuthor:
                PostAuthor = PostAuthor[:PostAuthor.find('鎖')].strip()
                LockPost = True
            PostAuthor = PostAuthor[PostAuthor.rfind(' '):].strip()

            PostTitle = CursorLine
            if ' □ ' in PostTitle:
                PostTitle = PostTitle[PostTitle.find('□') + 1:].strip()
            elif ' R:' in PostTitle:
                PostTitle = PostTitle[PostTitle.find('R:'):].strip()
            elif ' 轉 ' in PostTitle:
                # print(f'[{PostTitle}]=========>')
                PostTitle = PostTitle[PostTitle.find('轉') + 1:].strip()
                PostTitle = f'Fw: {PostTitle}'
                # print(f'=========>[{PostTitle}]')
            elif ' 鎖 ' in PostTitle:
                PostTitle = PostTitle[PostTitle.find('鎖') + 1:].strip()

            OriScreenTemp = OriScreen[OriScreen.find('┌──────────'):]
            OriScreenTemp = OriScreenTemp[:OriScreenTemp.find(
                '└─────────────')
            ]

            AIDLine = [line for line in OriScreen.split(
                '\n') if line.startswith('│ 文章代碼(AID)')]

            if len(AIDLine) == 1:
                AIDLine = AIDLine[0]
                pattern = re.compile('#[\w|-]+')
                PatternResult = pattern.search(AIDLine)
                PostAID = PatternResult.group(0)[1:]

            pattern = re.compile('文章網址: https:[\S]+html')
            PatternResult = pattern.search(OriScreenTemp)
            if PatternResult is None:
                PostWeb = None
            else:
                PostWeb = PatternResult.group(0)[6:]

            pattern = re.compile('這一篇文章值 [\d]+ Ptt幣')
            PatternResult = pattern.search(OriScreenTemp)
            if PatternResult is None:
                # 特殊文章無價格
                PostMoney = -1
            else:
                PostMoney = PatternResult.group(0)[7:]
                PostMoney = PostMoney[:PostMoney.find(' ')]
                PostMoney = int(PostMoney)

            pattern = re.compile('[\d]+\/[\d]+')
            PatternResult = pattern.search(CursorLine)
            if PatternResult is None:
                ListDate = None
            else:
                ListDate = PatternResult.group(0)
                ListDate = ListDate[-5:]

            # >  7485   9 8/09 CodingMan    □ [閒聊] PTT Library 更新
            # > 79189 M 1 9/17 LittleCalf   □ [公告] 禁言退文公告
            # >781508 +爆 9/17 jodojeda     □ [新聞] 國人吃魚少 學者：應把吃魚當成輕鬆愉快
            # >781406 +X1 9/17 kingofage111 R: [申請] ReDmango 請辭Gossiping板主職務

            PushNumber = CursorLine
            # print(PushNumber)
            PushNumber = PushNumber[:PushNumber.find(ListDate)]
            # print(PushNumber)
            PushNumber = PushNumber[7:]
            # print(PushNumber)
            PushNumber = PushNumber.split(' ')
            # print(PushNumber)
            PushNumber = list(filter(None, PushNumber))
            # print(PushNumber)

            if len(PushNumber) == 0:
                PushNumber = None
            else:
                PushNumber = PushNumber[-1]
                # print(PushNumber)

                if PushNumber.startswith('+') or PushNumber.startswith('~'):
                    PushNumber = PushNumber[1:]
                    # print(PushNumber)
                if PushNumber.lower().startswith('m'):
                    PushNumber = PushNumber[1:]
                    # print(PushNumber)
                if PushNumber.lower().startswith('!'):
                    PushNumber = PushNumber[1:]

                if PushNumber.lower().startswith('s'):
                    PushNumber = PushNumber[1:]

                if len(PushNumber) == 0:
                    PushNumber = None

            # print(PushNumber)
            Log.showValue(Log.Level.DEBUG, 'PostAuthor', PostAuthor)
            Log.showValue(Log.Level.DEBUG, 'PostTitle', PostTitle)
            Log.showValue(Log.Level.DEBUG, 'PostAID', PostAID)
            Log.showValue(Log.Level.DEBUG, 'PostWeb', PostWeb)
            Log.showValue(Log.Level.DEBUG, 'PostMoney', PostMoney)
            Log.showValue(Log.Level.DEBUG, 'ListDate', ListDate)
            Log.showValue(Log.Level.DEBUG, 'PushNumber', PushNumber)

            if LockPost:
                Post = DataType.PostInfo(
                    Board=Board,
                    AID=PostAID,
                    Author=PostAuthor,
                    Title=PostTitle,
                    WebUrl=PostWeb,
                    Money=PostMoney,
                    ListDate=ListDate,
                    FormatCheck=True,
                    PushNumber=PushNumber,
                    Lock=True,
                )
                return Post

        if Query:
            Post = DataType.PostInfo(
                Board=Board,
                AID=PostAID,
                Author=PostAuthor,
                Title=PostTitle,
                WebUrl=PostWeb,
                Money=PostMoney,
                ListDate=ListDate,
                FormatCheck=True,
                PushNumber=PushNumber,
            )
            return Post

        Cmd = Command.Enter * 2
        TargetList = [
            ConnectCore.TargetUnit(
                [
                    i18n.BrowsePost,
                    i18n.Done,
                ],
                Screens.Target.PostEnd,
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.BrowsePost,
                ],
                Screens.Target.InPost,
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.PostNoContent,
                ],
                Screens.Target.PostNoContent,
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
        ]

        LineFromTopattern = re.compile('[\d]+~[\d]+')

        ContentStart = '───────────────────────────────────────'
        ContentEnd = '--\n※ 發信站: 批踢踢實業坊(ptt.cc)'

        HasControlCode = False
        ControlCodeMode = False
        PushStart = False

        FirstPage = True
        OriginPost = []
        while True:
            index = self._ConnectCore.send(Cmd, TargetList)

            if index == 2:
                Post = DataType.PostInfo(
                    Board=Board,
                    AID=PostAID,
                    Author=PostAuthor,
                    # Date=PostDate,
                    Title=PostTitle,
                    WebUrl=PostWeb,
                    Money=PostMoney,
                    # Content=PostContent,
                    # PushList=PushList,
                    ListDate=ListDate,
                    ControlCode=HasControlCode,
                    FormatCheck=False,
                    PushNumber=PushNumber,
                )
                return Post
            LastScreen = self._ConnectCore.getScreenQueue()[-1]
            Lines = LastScreen.split('\n')
            LastLine = Lines[-1]
            Lines.pop()
            LastScreen = '\n'.join(Lines)

            PatternResult = LineFromTopattern.search(LastLine)
            if PatternResult is None:
                ControlCodeMode = True
                HasControlCode = True
            else:
                LastReadLineTemp = int(PatternResult.group(0).split('~')[1])
                if ControlCodeMode:
                    LastReadLine = LastReadLineTemp - 1
                ControlCodeMode = False

            if FirstPage:
                FirstPage = False
                OriginPost.append(LastScreen)
            else:
                if not ControlCodeMode:
                    GetLine = LastReadLineTemp - LastReadLine
                    if GetLine > 0:
                        NewContentPart = '\n'.join(Lines[-GetLine:])
                    else:
                        NewContentPart = '\n'.join(Lines)
                else:
                    NewContentPart = Lines[-1]

                OriginPost.append(NewContentPart)
                Log.showValue(
                    Log.Level.DEBUG,
                    'NewContentPart',
                    NewContentPart
                )

            if index == 0:
                break

            if not ControlCodeMode:
                LastReadLine = LastReadLineTemp

            if ContentEnd in LastScreen:
                PushStart = True

            if not PushStart:
                Cmd = Command.Down
            else:
                Cmd = Command.Right

        OriginPost = '\n'.join(OriginPost)

        Log.showValue(
            Log.Level.DEBUG,
            'OriginPost',
            OriginPost
        )

        # print('=' * 20)
        # print()
        # print('=' * 20)

        PostAuthorPattern_New = re.compile('作者  (.+) 看板')
        PostAuthorPattern_Old = re.compile('作者  (.+)')
        BoardPattern = re.compile('看板  (.+)')

        PostDate = None
        PostContent = []
        IP = None
        Location = None
        PushList = []

        # 格式確認，亂改的我也沒辦法Q_Q
        OriginPostLines = OriginPost.split('\n')

        AuthorLine = OriginPostLines[0]

        if Board.lower() == 'allpost':
            BoardLine = AuthorLine[AuthorLine.find(')') + 1:]
            PatternResult = BoardPattern.search(BoardLine)
            if PatternResult is not None:
                BoardTemp = PostAuthor = PatternResult.group(0)
                BoardTemp = BoardTemp[2:].strip()
                if len(BoardTemp) > 0:
                    Board = BoardTemp
                    Log.showValue(
                        Log.Level.DEBUG,
                        i18n.Board,
                        Board
                    )
        PatternResult = PostAuthorPattern_New.search(AuthorLine)
        if PatternResult is not None:
            PostAuthor = PatternResult.group(0)
            PostAuthor = PostAuthor[:PostAuthor.rfind(')') + 1]
        else:
            PatternResult = PostAuthorPattern_Old.search(AuthorLine)
            if PatternResult is None:
                Log.showValue(
                    Log.Level.DEBUG,
                    i18n.SubstandardPost,
                    i18n.Author
                )
                Post = DataType.PostInfo(
                    Board=Board,
                    AID=PostAID,
                    Author=PostAuthor,
                    Date=PostDate,
                    Title=PostTitle,
                    WebUrl=PostWeb,
                    Money=PostMoney,
                    Content=PostContent,
                    IP=IP,
                    PushList=PushList,
                    ListDate=ListDate,
                    ControlCode=HasControlCode,
                    FormatCheck=False,
                    Location=Location,
                    PushNumber=PushNumber,
                    OriginPost=OriginPost,
                )
                return Post
            PostAuthor = PatternResult.group(0)
            PostAuthor = PostAuthor[:PostAuthor.rfind(')') + 1]
        PostAuthor = PostAuthor[4:].strip()

        Log.showValue(
            Log.Level.DEBUG,
            i18n.Author,
            PostAuthor
        )

        PostTitlePattern = re.compile('標題  (.+)')

        TitleLine = OriginPostLines[1]
        PatternResult = PostTitlePattern.search(TitleLine)
        if PatternResult is None:
            Log.showValue(
                Log.Level.DEBUG,
                i18n.SubstandardPost,
                i18n.Title
            )
            Post = DataType.PostInfo(
                Board=Board,
                AID=PostAID,
                Author=PostAuthor,
                Date=PostDate,
                Title=PostTitle,
                WebUrl=PostWeb,
                Money=PostMoney,
                Content=PostContent,
                IP=IP,
                PushList=PushList,
                ListDate=ListDate,
                ControlCode=HasControlCode,
                FormatCheck=False,
                Location=Location,
                PushNumber=PushNumber,
                OriginPost=OriginPost,
            )
            return Post
        PostTitle = PatternResult.group(0)
        PostTitle = PostTitle[4:].strip()

        Log.showValue(
            Log.Level.DEBUG,
            i18n.Title,
            PostTitle
        )

        PostDatePattern = re.compile('時間  (.+)')
        DateLine = OriginPostLines[2]
        PatternResult = PostDatePattern.search(DateLine)
        if PatternResult is None:
            Log.showValue(
                Log.Level.DEBUG,
                i18n.SubstandardPost,
                i18n.Date
            )
            Post = DataType.PostInfo(
                Board=Board,
                AID=PostAID,
                Author=PostAuthor,
                Date=PostDate,
                Title=PostTitle,
                WebUrl=PostWeb,
                Money=PostMoney,
                Content=PostContent,
                IP=IP,
                PushList=PushList,
                ListDate=ListDate,
                ControlCode=HasControlCode,
                FormatCheck=False,
                Location=Location,
                PushNumber=PushNumber,
                OriginPost=OriginPost,
            )
            return Post
        PostDate = PatternResult.group(0)
        PostDate = PostDate[4:].strip()

        Log.showValue(
            Log.Level.DEBUG,
            i18n.Date,
            PostDate
        )

        if ContentStart in OriginPost and ContentEnd in OriginPost:
            PostContent = OriginPost
            PostContent = PostContent[
                PostContent.find(ContentStart) +
                len(ContentStart):
            ]
            PostContent = PostContent[
                :PostContent.rfind('※ 發信站: 批踢踢實業坊(ptt.cc)')
            ]
            PostContent = PostContent.strip()
        else:
            Log.showValue(
                Log.Level.DEBUG,
                i18n.SubstandardPost,
                i18n.Content
            )
            Post = DataType.PostInfo(
                Board=Board,
                AID=PostAID,
                Author=PostAuthor,
                Date=PostDate,
                Title=PostTitle,
                WebUrl=PostWeb,
                Money=PostMoney,
                Content=PostContent,
                IP=IP,
                PushList=PushList,
                ListDate=ListDate,
                ControlCode=HasControlCode,
                FormatCheck=False,
                Location=Location,
                PushNumber=PushNumber,
                OriginPost=OriginPost,
            )
            return Post

        Log.showValue(
            Log.Level.DEBUG,
            i18n.Content,
            PostContent
        )

        OriginPostLines = OriginPost[OriginPost.find(ContentEnd):]
        OriginPostLines = OriginPostLines.split('\n')

        InfoLines = [
            line for line in OriginPostLines if line.startswith('※') or line.startswith('◆')
        ]
        pattern = re.compile('[\d]+\.[\d]+\.[\d]+\.[\d]+')

        for line in reversed(InfoLines):
            Log.showValue(
                Log.Level.DEBUG,
                'IP Line',
                line
            )

            # type 1
            # ※ 編輯: CodingMan (111.243.146.98 臺灣)
            # ※ 發信站: 批踢踢實業坊(ptt.cc), 來自: 111.243.146.98 (臺灣)

            # type 2
            # ※ 發信站: 批踢踢實業坊(ptt.cc), 來自: 116.241.32.178
            # ※ 編輯: kill77845 (114.136.55.237), 12/08/2018 16:47:59

            # type 3
            # ※ 發信站: 批踢踢實業坊(ptt.cc)
            # ◆ From: 211.20.78.69
            # ※ 編輯: JCC             來自: 211.20.78.69         (06/20 10:22)
            # ※ 編輯: JCC (118.163.28.150), 12/03/2015 14:25:35

            PatternResult = pattern.search(line)
            if PatternResult is not None:
                IP = PatternResult.group(0)
                LocationTemp = line[line.find(IP) + len(IP):].strip()
                LocationTemp = LocationTemp.replace('(', '')
                LocationTemp = LocationTemp[:LocationTemp.rfind(')')]
                # print(f'=>[{LocationTemp}]')
                if ' ' not in LocationTemp:
                    Location = LocationTemp
                    Log.showValue(Log.Level.DEBUG, 'Location', Location)
                break

        if IP is None:
            Log.showValue(
                Log.Level.DEBUG,
                i18n.SubstandardPost,
                'IP'
            )
            Post = DataType.PostInfo(
                Board=Board,
                AID=PostAID,
                Author=PostAuthor,
                Date=PostDate,
                Title=PostTitle,
                WebUrl=PostWeb,
                Money=PostMoney,
                Content=PostContent,
                IP=IP,
                PushList=PushList,
                ListDate=ListDate,
                ControlCode=HasControlCode,
                FormatCheck=False,
                Location=Location,
                PushNumber=PushNumber,
                OriginPost=OriginPost,
            )
            return Post
        Log.showValue(Log.Level.DEBUG, 'IP', IP)

        PushAuthorPattern = re.compile('[推|噓|→] [\w| ]+:')
        PushDatePattern = re.compile('[\d]+/[\d]+ [\d]+:[\d]+')
        PushIPPattern = re.compile('[\d]+\.[\d]+\.[\d]+\.[\d]+')

        PushList = []

        for line in OriginPostLines:
            PushType = 0
            if line.startswith('推'):
                PushType = DataType.PushType.Push
            elif line.startswith('噓 '):
                PushType = DataType.PushType.Boo
            elif line.startswith('→ '):
                PushType = DataType.PushType.Arrow
            else:
                continue

            Result = PushAuthorPattern.search(line)
            if Result is None:
                # 不符合推文格式
                continue
            PushAuthor = Result.group(0)[2:-1].strip()
            Log.showValue(Log.Level.DEBUG, [
                i18n.Push,
                i18n.ID,
            ],
                PushAuthor
            )

            Result = PushDatePattern.search(line)
            if Result is None:
                continue
            PushDate = Result.group(0)
            Log.showValue(Log.Level.DEBUG, [
                i18n.Push,
                i18n.Date,
            ],
                PushDate
            )

            PushIP = None
            Result = PushIPPattern.search(line)
            if Result is not None:
                PushIP = Result.group(0)
                Log.showValue(Log.Level.DEBUG, [
                    i18n.Push,
                    'IP',
                ],
                    PushIP
                )

            PushContent = line[
                line.find(PushAuthor) + len(PushAuthor):
            ]
            PushContent = PushContent.replace(PushDate, '')
            if PushIP is not None:
                PushContent = PushContent.replace(PushIP, '')
            PushContent = PushContent[
                PushContent.find(':') + 1:
            ].strip()
            Log.showValue(Log.Level.DEBUG, [
                i18n.Push,
                i18n.Content,
            ],
                PushContent
            )

            CurrentPush = DataType.PushInfo(
                PushType,
                PushAuthor,
                PushContent,
                PushIP,
                PushDate
            )
            PushList.append(CurrentPush)

        Post = DataType.PostInfo(
            Board=Board,
            AID=PostAID,
            Author=PostAuthor,
            Date=PostDate,
            Title=PostTitle,
            WebUrl=PostWeb,
            Money=PostMoney,
            Content=PostContent,
            IP=IP,
            PushList=PushList,
            ListDate=ListDate,
            ControlCode=HasControlCode,
            FormatCheck=True,
            Location=Location,
            PushNumber=PushNumber,
            OriginPost=OriginPost,
        )
        return Post

    def _getNewestIndex(
        self,
        IndexType: int,
        Board: str = None,
        SearchType: int = 0,
        SearchCondition: str = None
    ):

        if not Util.checkRange(DataType.IndexType, IndexType):
            raise ValueError('Unknow IndexType', IndexType)

        if not isinstance(Board, str):
            raise TypeError(Log.merge([
                'Board',
                i18n.MustBe,
                i18n.String
            ]))
        if not isinstance(SearchType, int):
            raise TypeError(Log.merge([
                'SearchType',
                i18n.MustBe,
                i18n.Integer
            ]))
        if (SearchCondition is not None and
                not isinstance(SearchCondition, str)):
            raise TypeError(Log.merge([
                'SearchCondition',
                i18n.MustBe,
                i18n.String
            ]))
        if (SearchType != 0 and
                not Util.checkRange(DataType.PostSearchType, SearchType)):
            raise ValueError('Unknow PostSearchType', PostSearchType)

        if IndexType == DataType.IndexType.Board:
            CmdList = []
            CmdList.append(Command.GoMainMenu)
            CmdList.append('qs')
            CmdList.append(Board)
            CmdList.append(Command.Enter)
            CmdList.append(Command.Ctrl_C * 2)
            CmdList.append(Command.Space)

            if SearchCondition is not None:
                if SearchType == DataType.PostSearchType.Keyword:
                    CmdList.append('/')
                elif SearchType == DataType.PostSearchType.Author:
                    CmdList.append('a')
                elif SearchType == DataType.PostSearchType.Push:
                    CmdList.append('Z')
                elif SearchType == DataType.PostSearchType.Mark:
                    CmdList.append('G')
                elif SearchType == DataType.PostSearchType.Money:
                    CmdList.append('A')

                CmdList.append(SearchCondition)
                CmdList.append(Command.Enter)

            CmdList.append('1')
            CmdList.append(Command.Enter)
            CmdList.append('$')

            Cmd = ''.join(CmdList)

            TargetList = [
                ConnectCore.TargetUnit(
                    i18n.Success,
                    Screens.Target.InBoard,
                    BreakDetect=True,
                    LogLevel=Log.Level.DEBUG
                ),
                ConnectCore.TargetUnit(
                    i18n.Success,
                    Screens.Target.InBoardWithCursor,
                    BreakDetect=True,
                    LogLevel=Log.Level.DEBUG
                ),
            ]
            index = self._ConnectCore.send(Cmd, TargetList)
            if index < 0:
                OriScreen = self._ConnectCore.getScreenQueue()[-1]
                raise Exceptions.UnknowError(OriScreen)

            LastScreen = self._ConnectCore.getScreenQueue()[-1]
            AllIndex = re.findall(r'\d+ ', LastScreen)

            if len(AllIndex) == 0:
                Screens.show(self._ConnectCore.getScreenQueue())
                raise Exceptions.UnknowError(i18n.UnknowError)

            AllIndex = list(map(int, AllIndex))
            AllIndex.sort(reverse=True)

            MaxCheckRange = 6
            NewestIndex = 0
            for IndexTemp in AllIndex:
                Continue = True
                if IndexTemp > MaxCheckRange:
                    CheckRange = MaxCheckRange
                else:
                    CheckRange = IndexTemp
                for i in range(1, CheckRange):
                    if str(IndexTemp - i) not in LastScreen:
                        Continue = False
                        break
                if Continue:
                    Log.showValue(
                        Log.Level.DEBUG,
                        i18n.FindNewestIndex,
                        IndexTemp
                    )
                    NewestIndex = IndexTemp
                    break

            if NewestIndex == 0:
                Screens.show(self._ConnectCore.getScreenQueue())
                raise Exceptions.UnknowError(i18n.UnknowError)

        else:
            pass

        return NewestIndex

    def getNewestIndex(
        self,
        IndexType: int,
        Board: str = None,
        SearchType: int = 0,
        SearchCondition: str = None
    ):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        try:
            return self._getNewestIndex(
                IndexType,
                Board,
                SearchType,
                SearchCondition
            )
        except Exceptions.UnknowError:
            return self._getNewestIndex(
                IndexType,
                Board,
                SearchType,
                SearchCondition
            )

    def crawlBoard(
        self,
        PostHandler,
        Board: str,
        StartIndex: int = 0,
        EndIndex: int = 0,
        SearchType: int = 0,
        SearchCondition: str = None,
        Query: bool = False
    ):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if not isinstance(Board, str):
            raise TypeError(Log.merge([
                'Board',
                i18n.MustBe,
                i18n.String
            ]))

        if not isinstance(StartIndex, int):
            raise TypeError(Log.merge([
                'StartIndex',
                i18n.MustBe,
                i18n.Integer
            ]))
        if not isinstance(EndIndex, int):
            raise TypeError(Log.merge([
                'EndIndex',
                i18n.MustBe,
                i18n.Integer
            ]))
        if not isinstance(SearchType, int):
            raise TypeError(Log.merge([
                'SearchType',
                i18n.MustBe,
                i18n.Integer
            ]))
        if (SearchCondition is not None and
                not isinstance(SearchCondition, str)):
            raise TypeError(Log.merge([
                'SearchCondition',
                i18n.MustBe,
                i18n.String
            ]))

        if len(Board) == 0:
            raise ValueError(Log.merge([
                i18n.Board,
                i18n.ErrorParameter,
                Board
            ]))

        if StartIndex < 1:
            raise ValueError(Log.merge([
                'StartIndex',
                i18n.ErrorParameter,
                i18n.OutOfRange,
            ]))

        if StartIndex < 1:
            raise ValueError(Log.merge([
                'StartIndex',
                i18n.ErrorParameter,
                i18n.OutOfRange,
            ]))

        if StartIndex > EndIndex:
            raise ValueError(Log.merge([
                'StartIndex',
                i18n.MustSmall,
                'EndIndex',
            ]))

        if SearchType == DataType.PostSearchType.Push:
            try:
                S = int(SearchCondition)
            except ValueError:
                raise ValueError(Log.merge([
                    'SearchCondition',
                    i18n.ErrorParameter,
                ]))

            if not (-100 <= S <= 110):
                raise ValueError(Log.merge([
                    'SearchCondition',
                    i18n.ErrorParameter,
                ]))

        NewestIndex = self._getNewestIndex(
            DataType.IndexType.Board,
            Board=Board,
            SearchType=SearchType,
            SearchCondition=SearchCondition
        )

        if EndIndex > NewestIndex:
            raise ValueError(Log.merge([
                'EndIndex',
                i18n.ErrorParameter,
                i18n.OutOfRange,
            ]))

        ErrorPostList = []
        DelPostList = []
        if Config.LogLevel == Log.Level.INFO:
            PB = progressbar.ProgressBar(
                max_value=EndIndex - StartIndex + 1,
                redirect_stdout=True
            )
        for index in range(StartIndex, EndIndex + 1):

            for i in range(2):
                NeedContinue = False
                Post = None
                try:
                    Post = self._getPost(
                        Board,
                        PostIndex=index,
                        SearchType=SearchType,
                        SearchCondition=SearchCondition,
                        Query=Query
                    )
                except Exceptions.ParseError as e:
                    if i == 1:
                        raise e
                    NeedContinue = True
                except Exceptions.UnknowError as e:
                    if i == 1:
                        raise e
                    NeedContinue = True
                except Exceptions.NoSuchBoard as e:
                    if i == 1:
                        raise e
                    NeedContinue = True
                except ConnectCore.NoMatchTargetError as e:
                    if i == 1:
                        raise e
                    NeedContinue = True

                if Post is None:
                    NeedContinue = True
                elif not Post.isFormatCheck():
                    NeedContinue = True

                if NeedContinue:
                    Log.log(
                        Log.Level.DEBUG,
                        'Wait for retry repost'
                    )
                    time.sleep(0.1)
                    continue

                break

            if Config.LogLevel == Log.Level.INFO:
                PB.update(index - StartIndex)
            if Post is None:
                ErrorPostList.append(index)
                continue
            if not Post.isFormatCheck():
                if Post.getAID() is not None:
                    ErrorPostList.append(Post.getAID())
                else:
                    ErrorPostList.append(index)
                continue
            if Post.getDeleteStatus() != DataType.PostDeleteStatus.NotDeleted:
                DelPostList.append(index)
            PostHandler(Post)
        if Config.LogLevel == Log.Level.INFO:
            PB.finish()
        return ErrorPostList, DelPostList

    def post(
        self,
        Board: str,
        Title: str,
        Content: str,
        PostType: int,
        SignFile
    ):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if not isinstance(Board, str):
            raise TypeError(Log.merge([
                'Board',
                i18n.MustBe,
                i18n.String
            ]))

        if not isinstance(Title, str):
            raise TypeError(Log.merge([
                'Title',
                i18n.MustBe,
                i18n.String
            ]))

        if not isinstance(Content, str):
            raise TypeError(Log.merge([
                'Content',
                i18n.MustBe,
                i18n.String
            ]))

        if not isinstance(PostType, int):
            raise TypeError(Log.merge([
                'PostType',
                i18n.MustBe,
                i18n.Integer
            ]))

        CheckSignFile = False
        for i in range(0, 10):
            if str(i) == SignFile or i == SignFile:
                CheckSignFile = True
                break

        if not CheckSignFile:
            SignFile = SignFile.lower()
            if SignFile != 'x':
                raise ValueError(Log.merge([
                    'SignFile',
                    i18n.ErrorParameter,
                    SignFile
                ]))

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('qs')
        CmdList.append(Board)
        CmdList.append(Command.Enter)
        CmdList.append(Command.Ctrl_C * 2)
        CmdList.append(Command.Space)
        CmdList.append(Command.Ctrl_P)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                i18n.HasPostPermission,
                '發表文章於【',
                BreakDetect=True,
            ),
            ConnectCore.TargetUnit(
                i18n.NoPermission,
                '使用者不可發言',
                BreakDetect=True,
            )
        ]
        index = self._ConnectCore.send(Cmd, TargetList)
        if index < 0:
            Screens.show(self._ConnectCore.getScreenQueue())
            raise Exceptions.UnknowError(i18n.UnknowError)
        if index == 1:
            raise Exceptions.NoPermission(i18n.NoPermission)

        Screens.show(self._ConnectCore.getScreenQueue())

        CmdList = []
        CmdList.append(str(PostType))
        CmdList.append(Command.Enter)
        CmdList.append(str(Title))
        CmdList.append(Command.Enter)
        CmdList.append(str(Content))
        CmdList.append(Command.Ctrl_X)
        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                i18n.AnyKeyContinue,
                '任意鍵繼續',
                BreakDetect=True,
            ),
            ConnectCore.TargetUnit(
                i18n.SaveFile,
                '確定要儲存檔案嗎',
                Response='s' + Command.Enter,
            ),
            ConnectCore.TargetUnit(
                i18n.SelectSignature,
                'x=隨機',
                Response=str(SignFile) + Command.Enter,
            ),
        ]
        index = self._ConnectCore.send(Cmd, TargetList)

    def push(
        self,
        Board: str,
        PushType: int,
        PushContent: str,
        PostAID: str = None,
        PostIndex: int = 0
    ):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if not isinstance(Board, str):
            raise TypeError(Log.merge([
                'Board',
                i18n.MustBe,
                i18n.String
            ]))
        if not isinstance(PushType, int):
            raise TypeError(Log.merge([
                'PushType',
                i18n.MustBe,
                i18n.Integer
            ]))
        if not isinstance(PushContent, str):
            raise TypeError(Log.merge([
                'PushContent',
                i18n.MustBe,
                i18n.String
            ]))
        if not isinstance(PostAID, str) and PostAID is not None:
            raise TypeError(Log.merge([
                'PostAID',
                i18n.MustBe,
                i18n.String
            ]))
        if not isinstance(PostIndex, int):
            raise TypeError(Log.merge([
                'PostIndex',
                i18n.MustBe,
                i18n.Integer
            ]))
        if len(Board) == 0:
            raise ValueError(Log.merge([
                i18n.Board,
                i18n.ErrorParameter,
                Board
            ]))
        if not Util.checkRange(DataType.PushType, PushType):
            raise ValueError('Unknow PushType', PushType)
        if PostIndex != 0 and isinstance(PostAID, str):
            raise ValueError(Log.merge([
                'PostIndex',
                'PostAID',
                i18n.ErrorParameter,
                i18n.BothInput
            ]))

        if PostIndex == 0 and PostAID is None:
            raise ValueError(Log.merge([
                'PostIndex',
                'PostAID',
                i18n.ErrorParameter,
                i18n.NoInput
            ]))
        if PostIndex > 0:
            NewestIndex = self._getNewestIndex(
                DataType.IndexType.Board,
                Board=Board
            )

            if PostIndex > NewestIndex:
                raise ValueError(Log.merge([
                    'PostIndex',
                    i18n.ErrorParameter,
                    i18n.OutOfRange,
                ]))

        MaxPushLength = 33
        PushList = []

        TempStartIndex = 0
        TempEndIndex = TempStartIndex + 1

        while TempEndIndex <= len(PushContent):

            Temp = ''
            LastTemp = None
            while len(Temp.encode('big5-uao', 'replace')) < MaxPushLength:
                Temp = PushContent[TempStartIndex:TempEndIndex]

                if not len(Temp.encode('big5-uao', 'replace')) < MaxPushLength:
                    break
                elif PushContent.endswith(Temp):
                    break
                elif Temp.endswith('\n'):
                    break
                elif LastTemp == Temp:
                    break

                TempEndIndex += 1
                LastTemp = Temp

            PushList.append(Temp.strip())

            TempStartIndex = TempEndIndex
            TempEndIndex = TempStartIndex + 1
        PushList = filter(None, PushList)

        for push in PushList:
            Log.showValue(
                Log.Level.INFO,
                i18n.Push,
                push
            )

            for _ in range(2):
                try:
                    self._push(
                        Board,
                        PushType,
                        push,
                        PostAID=PostAID,
                        PostIndex=PostIndex
                    )
                    break
                except Exceptions.NoFastPush:
                    # Screens.show(self._ConnectCore.getScreenQueue())
                    Log.log(
                        Log.Level.INFO,
                        '等待快速推文'
                    )
                    time.sleep(5.2)

    def _push(
        self,
        Board: str,
        PushType: int,
        PushContent: str,
        PostAID: str = None,
        PostIndex: int = 0
    ):
        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('qs')
        CmdList.append(Board)
        CmdList.append(Command.Enter)
        CmdList.append(Command.Ctrl_C * 2)
        CmdList.append(Command.Space)

        if PostAID is not None:
            CmdList.append('#' + PostAID)
        elif PostIndex != 0:
            CmdList.append(str(PostIndex))
        CmdList.append(Command.Enter)
        CmdList.append(Command.Push)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                i18n.HasPushPermission,
                '您覺得這篇',
                LogLevel=Log.Level.DEBUG,
                BreakDetect=True
            ),
            ConnectCore.TargetUnit(
                i18n.OnlyArrow,
                '加註方式',
                LogLevel=Log.Level.DEBUG,
                BreakDetect=True
            ),
            ConnectCore.TargetUnit(
                i18n.NoFastPush,
                '禁止快速連續推文',
                LogLevel=Log.Level.INFO,
                BreakDetect=True,
                Exceptions=Exceptions.NoFastPush()
            ),
            ConnectCore.TargetUnit(
                i18n.NoFastPush,
                '禁止短時間內大量推文',
                LogLevel=Log.Level.INFO,
                BreakDetect=True,
                Exceptions=Exceptions.NoFastPush()
            ),
            ConnectCore.TargetUnit(
                i18n.NoPermission,
                '使用者不可發言',
                LogLevel=Log.Level.INFO,
                BreakDetect=True,
                Exceptions=Exceptions.Error(i18n.NoPermission)
            )
        ]

        index = self._ConnectCore.send(
            Cmd,
            TargetList
        )

        # print(index)
        # print(self._ConnectCore.getScreenQueue()[-1].split('\n')[-1])

        EnablePush = False
        EnableBoo = False
        EnableArrow = False

        CmdList = []

        if index == 0:
            PushOptionLine = self._ConnectCore.getScreenQueue()[-1]
            PushOptionLine = PushOptionLine.split('\n')[-1]
            Log.showValue(Log.Level.DEBUG, 'Push option line', PushOptionLine)

            EnablePush = '值得推薦' in PushOptionLine
            EnableBoo = '給它噓聲' in PushOptionLine
            EnableArrow = '只加→註解' in PushOptionLine

            Log.showValue(Log.Level.DEBUG, 'Push', EnablePush)
            Log.showValue(Log.Level.DEBUG, 'Boo', EnableBoo)
            Log.showValue(Log.Level.DEBUG, 'Arrow', EnableArrow)

            if PushType == DataType.PushType.Push and not EnablePush:
                PushType = DataType.PushType.Arrow
            elif PushType == DataType.PushType.Boo and not EnableBoo:
                PushType = DataType.PushType.Arrow
            elif PushType == DataType.PushType.Arrow and not EnableArrow:
                PushType = DataType.PushType.Push

            CmdList.append(str(PushType))
        elif index == 1:
            PushType = DataType.PushType.Arrow

        CmdList.append(PushContent)
        CmdList.append(Command.Enter)
        CmdList.append('y')
        CmdList.append(Command.Enter)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                [
                    i18n.Push,
                    i18n.Success,
                ],
                Screens.Target.InBoard,
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
        ]

        index = self._ConnectCore.send(
            Cmd,
            TargetList
        )

    def _getUser(self, UserID):

        if not isinstance(UserID, str):
            raise TypeError(Log.merge([
                'UserID',
                i18n.MustBe,
                i18n.String
            ]))

        if len(UserID) < 3:
            raise ValueError(Log.merge([
                'UserID',
                i18n.ErrorParameter,
                UserID
            ]))

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('T')
        CmdList.append(Command.Enter)
        CmdList.append('Q')
        CmdList.append(Command.Enter)
        CmdList.append(UserID)
        CmdList.append(Command.Enter)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                [
                    i18n.GetUser,
                    i18n.Success,
                ],
                Screens.Target.AnyKey,
                BreakDetect=True,
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.GetUser,
                    i18n.Fail,
                ],
                Screens.Target.InTalk,
                BreakDetect=True,
            ),
        ]

        index = self._ConnectCore.send(
            Cmd,
            TargetList
        )
        OriScreen = self._ConnectCore.getScreenQueue()[-1]
        Log.showValue(
            Log.Level.DEBUG,
            'OriScreen',
            OriScreen
        )
        if index == 1:
            raise Exceptions.NoSuchUser(UserID)

        Data = Util.getSubStringList(OriScreen, '》', ['《', '\n'])
        if len(Data) < 10:
            print('\n'.join(Data))
            print(len(Data))
            raise Exceptions.ParseError(OriScreen)

        ID = Data[0]
        Money = Data[1]
        LoginTime = Data[2]
        LoginTime = LoginTime[:LoginTime.find(' ')]
        LoginTime = int(LoginTime)

        Temp = re.findall(r'\d+', Data[3])
        LegalPost = int(Temp[0])
        IllegalPost = int(Temp[1])

        State = Data[4]
        Mail = Data[5]
        LastLogin = Data[6]
        LastIP = Data[7]
        FiveChess = Data[8]
        Chess = Data[9]

        SignatureFile = '\n'.join(OriScreen.split('\n')[6:-1]).strip()

        Log.showValue(Log.Level.DEBUG, 'ID', ID)
        Log.showValue(Log.Level.DEBUG, 'Money', Money)
        Log.showValue(Log.Level.DEBUG, 'LoginTime', LoginTime)
        Log.showValue(Log.Level.DEBUG, 'LegalPost', LegalPost)
        Log.showValue(Log.Level.DEBUG, 'IllegalPost', IllegalPost)
        Log.showValue(Log.Level.DEBUG, 'State', State)
        Log.showValue(Log.Level.DEBUG, 'Mail', Mail)
        Log.showValue(Log.Level.DEBUG, 'LastLogin', LastLogin)
        Log.showValue(Log.Level.DEBUG, 'LastIP', LastIP)
        Log.showValue(Log.Level.DEBUG, 'FiveChess', FiveChess)
        Log.showValue(Log.Level.DEBUG, 'Chess', Chess)
        Log.showValue(Log.Level.DEBUG, 'SignatureFile', SignatureFile)

        User = DataType.UserInfo(
            ID,
            Money,
            LoginTime,
            LegalPost,
            IllegalPost,
            State,
            Mail,
            LastLogin,
            LastIP,
            FiveChess,
            Chess,
            SignatureFile
        )
        return User

    def getUser(self, UserID):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if self._UnregisteredUser:
            raise Exceptions.UnregisteredUser(Util.getCurrentFuncName())

        return self._getUser(UserID)

    def throwWaterBall(self, TargetID, Content):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if self._UnregisteredUser:
            raise Exceptions.UnregisteredUser(Util.getCurrentFuncName())

        if not isinstance(TargetID, str):
            raise TypeError(Log.merge([
                'TargetID',
                i18n.MustBe,
                i18n.String
            ]))

        if not isinstance(Content, str):
            raise TypeError(Log.merge([
                'Content',
                i18n.MustBe,
                i18n.String
            ]))

        if len(TargetID) <= 2:
            raise ValueError(Log.merge([
                'TargetID',
                i18n.ErrorParameter,
                TargetID
            ]))

        User = self._getUser(TargetID)
        if '不在站上' in User.getState():
            raise Exceptions.UserOffline(TargetID)

        MaxLength = 50

        WaterBallList = []

        TempStartIndex = 0
        TempEndIndex = TempStartIndex + 1

        while TempEndIndex <= len(Content):
            Temp = ''
            LastTemp = None
            while len(Temp.encode('big5-uao', 'ignore')) < MaxLength:
                Temp = Content[TempStartIndex:TempEndIndex]

                if not len(Temp.encode('big5-uao', 'ignore')) < MaxLength:
                    break
                elif Content.endswith(Temp) and TempStartIndex != 0:
                    break
                elif Temp.endswith('\n'):
                    break
                elif LastTemp == Temp:
                    break

                TempEndIndex += 1
                LastTemp = Temp

            WaterBallList.append(Temp.strip())

            TempStartIndex = TempEndIndex
            TempEndIndex = TempStartIndex + 1
        WaterBallList = filter(None, WaterBallList)

        for waterball in WaterBallList:

            if self._LastThroWaterBallTime != 0:
                CurrentTime = time.time()
                while (CurrentTime - self._LastThroWaterBallTime) < 3.2:
                    time.sleep(0.1)
                    CurrentTime = time.time()

            Log.showValue(
                Log.Level.INFO,
                i18n.WaterBall,
                waterball
            )

            TargetList = [
                ConnectCore.TargetUnit(
                    i18n.SetCallStatus,
                    '您的呼叫器目前設定為關閉',
                    Response='y' + Command.Enter,
                ),
                # 對方已落跑了
                ConnectCore.TargetUnit(
                    i18n.SetCallStatus,
                    '◆ 糟糕! 對方已落跑了',
                    Exceptions=Exceptions.UserOffline(TargetID)
                ),
                ConnectCore.TargetUnit(
                    [
                        i18n.Throw,
                        TargetID,
                        i18n.WaterBall
                    ],
                    '丟 ' + TargetID + ' 水球:',
                    Response=waterball + Command.Enter * 2 +
                    Command.GoMainMenu,
                ),
                ConnectCore.TargetUnit(
                    [
                        i18n.Throw,
                        i18n.WaterBall,
                        i18n.Success
                    ],
                    Screens.Target.MainMenu,
                    BreakDetect=True
                )
            ]

            CmdList = []
            CmdList.append(Command.GoMainMenu)
            CmdList.append('T')
            CmdList.append(Command.Enter)
            CmdList.append('U')
            CmdList.append(Command.Enter)
            if '【好友列表】' in self._ConnectCore.getScreenQueue()[-1]:
                CmdList.append('f')
            CmdList.append('s')
            CmdList.append(TargetID)
            CmdList.append(Command.Enter)
            CmdList.append('w')

            Cmd = ''.join(CmdList)

            index = self._ConnectCore.send(
                Cmd,
                TargetList,
                ScreenTimeout=Config.ScreenLongTimeOut
            )

            self._LastThroWaterBallTime = time.time()

    def getWaterBall(self, OperateType):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if self._UnregisteredUser:
            raise Exceptions.UnregisteredUser(Util.getCurrentFuncName())

        if not isinstance(OperateType, int):
            raise TypeError(Log.merge([
                'OperateType',
                i18n.MustBe,
                i18n.Integer
            ]))

        if not Util.checkRange(DataType.WaterBallOperateType, OperateType):
            raise ValueError('Unknow WaterBallOperateType', OperateType)

        if OperateType == DataType.WaterBallOperateType.DoNothing:
            WaterBallOperateType = 'R'
        elif OperateType == DataType.WaterBallOperateType.Clear:
            WaterBallOperateType = 'C' + Command.Enter + 'Y'
        elif OperateType == DataType.WaterBallOperateType.Mail:
            WaterBallOperateType = 'M'

        TargetList = [
            ConnectCore.TargetUnit(
                i18n.NoWaterball,
                '◆ 暫無訊息記錄',
                BreakDetect=True
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.BrowseWaterball,
                    i18n.Done,
                ],
                Screens.Target.WaterBallListEnd,
                Response=Command.Left + WaterBallOperateType +
                Command.Enter + Command.GoMainMenu,
                BreakDetectAfterSend=True,
                LogLevel=Log.Level.DEBUG
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.BrowseWaterball,
                ],
                Screens.Target.InWaterBallList,
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
        ]

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('T')
        CmdList.append(Command.Enter)
        CmdList.append('D')
        CmdList.append(Command.Enter)

        Cmd = ''.join(CmdList)

        WaterBallList = []

        LineFromTopattern = re.compile('[\d]+~[\d]+')
        ToWaterBallTargetPattern = re.compile('To [\w]+:')
        FromWaterBallTargetPattern = re.compile('★[\w]+ ')
        WaterBallDatePattern = re.compile(
            '\[[\d]+/[\d]+/[\d]+ [\d]+:[\d]+:[\d]+\]')

        LastReadLine = 0
        AddTailNextRound = False
        while True:
            index = self._ConnectCore.send(
                Cmd,
                TargetList,
                ScreenTimeout=1
            )
            Log.showValue(
                Log.Level.DEBUG,
                'index',
                index
            )
            if index == 0:
                return WaterBallList

            OriScreen = self._ConnectCore.getScreenQueue()[-1]

            # print(OriScreen)
            # print('=' * 50)
            ScreenTemp = OriScreen
            Log.showValue(
                Log.Level.DEBUG,
                'OriScreen',
                OriScreen
            )

            LastLine = ScreenTemp.split('\n')[-1].strip()
            Log.showValue(
                Log.Level.DEBUG,
                'LastLine',
                LastLine
            )
            if LastLine.startswith('★'):
                continue

            ScreenTemp = '\n'.join(ScreenTemp.split('\n')[:-1])

            # 整理水球換行格式
            ScreenTemp = ScreenTemp.replace(
                ']\n', ']==PTTWaterBallNewLine==')
            ScreenTemp = ScreenTemp.replace('\n', '')
            ScreenTemp = ScreenTemp.replace(
                ']==PTTWaterBallNewLine==', ']\n')

            # print('=' * 50)
            # print(LastLine)
            # print('=' * 50)

            Lines = ScreenTemp.split('\n')
            PatternResult = LineFromTopattern.search(LastLine)
            LastReadLineTemp = int(PatternResult.group(0).split('~')[1])
            GetLine = LastReadLineTemp - LastReadLine

            # print(LastReadLine)
            # print(GetLine)
            # print('=' * 50)
            if GetLine > 0 and LastReadLine != 0:
                if AddTailNextRound:
                    Log.log(
                        Log.Level.DEBUG,
                        'Add Tail'
                    )
                    AddTailNextRound = False
                    NewContentPart = Lines[-(GetLine + 1):]
                else:
                    NewContentPart = Lines[-GetLine:]
            else:
                NewContentPart = Lines
            NewContentPart = [x.strip() for x in NewContentPart]

            # print('\n'.join(NewContentPart))

            for line in NewContentPart:
                # print(f'line =>{line}<')
                # print(len(line))
                if len(line) == 0:
                    break
                if (not line.startswith('To')) and (not line.startswith('★')):

                    Log.showValue(
                        Log.Level.DEBUG,
                        'Discard waterball',
                        line
                    )
                    AddTailNextRound = True
                    continue

                if not line.endswith(']'):
                    Log.showValue(
                        Log.Level.DEBUG,
                        'Discard waterball',
                        line
                    )
                    AddTailNextRound = True
                    continue

                Log.showValue(
                    Log.Level.DEBUG,
                    'Ready to parse waterball',
                    line
                )

                if line.startswith('To'):
                    Log.showValue(
                        Log.Level.DEBUG,
                        'Waterball Type',
                        'Send'
                    )
                    Type = DataType.WaterBallType.Send

                    PatternResult = ToWaterBallTargetPattern.search(line)
                    Target = PatternResult.group(0)[3:-1]

                    PatternResult = WaterBallDatePattern.search(line)
                    Date = PatternResult.group(0)[1:-1]

                    Content = line
                    Content = Content[Content.find(
                        Target + ':') + len(Target + ':'):]
                    Content = Content[:Content.rfind(Date) - 1].strip()
                elif line.startswith('★'):
                    Log.showValue(
                        Log.Level.DEBUG,
                        'Waterball Type',
                        'Catch'
                    )
                    Type = DataType.WaterBallType.Catch

                    PatternResult = FromWaterBallTargetPattern.search(line)
                    Target = PatternResult.group(0)[1:-1]

                    PatternResult = WaterBallDatePattern.search(line)
                    Date = PatternResult.group(0)[1:-1]

                    Content = line
                    Content = Content[Content.find(
                        Target + ' ') + len(Target + ' '):]
                    Content = Content[:Content.rfind(Date) - 1].strip()

                Log.showValue(
                    Log.Level.DEBUG,
                    'Waterball Target',
                    Target
                )
                Log.showValue(
                    Log.Level.DEBUG,
                    'Waterball Content',
                    Content
                )
                Log.showValue(
                    Log.Level.DEBUG,
                    'Waterball Date',
                    Date
                )

                CurrentWaterBall = DataType.WaterBallInfo(
                    Type,
                    Target,
                    Content,
                    Date
                )

                WaterBallList.append(CurrentWaterBall)

            if index == 1:
                break
            # elif index == 2:
            #     pass

            Cmd = Command.Down
            LastReadLine = LastReadLineTemp

        return WaterBallList

    def getCallStatus(self):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        return self._getCallStatus()

    def _getCallStatus(self):

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('A')
        CmdList.append(Command.Right)
        CmdList.append(Command.Left)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                [
                    i18n.GetCallStatus,
                    i18n.Success,
                ],
                '[呼叫器]打開',
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.GetCallStatus,
                    i18n.Success,
                ],
                '[呼叫器]拔掉',
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.GetCallStatus,
                    i18n.Success,
                ],
                '[呼叫器]防水',
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.GetCallStatus,
                    i18n.Success,
                ],
                '[呼叫器]好友',
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.GetCallStatus,
                    i18n.Success,
                ],
                '[呼叫器]關閉',
                BreakDetect=True,
                LogLevel=Log.Level.DEBUG
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.GetCallStatus,
                ],
                '★',
                Response=Cmd,
                LogLevel=Log.Level.DEBUG
            ),
        ]

        index = self._ConnectCore.send(Cmd, TargetList)
        if index < 0:
            OriScreen = self._ConnectCore.getScreenQueue()[-1]
            raise Exceptions.UnknowError(OriScreen)

        if index == 0:
            return DataType.CallStatus.On
        if index == 1:
            return DataType.CallStatus.Unplug
        if index == 2:
            return DataType.CallStatus.Waterproof
        if index == 3:
            return DataType.CallStatus.Friend
        if index == 4:
            return DataType.CallStatus.Off

        OriScreen = self._ConnectCore.getScreenQueue()[-1]
        raise Exceptions.UnknowError(OriScreen)

    def setCallStatus(
        self,
        inputCallStatus
    ):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if not isinstance(inputCallStatus, int):
            raise TypeError('CallStatus must be integer')

        if not Util.checkRange(DataType.CallStatus, inputCallStatus):
            raise ValueError('Unknow CallStatus', inputCallStatus)

        # 打開 -> 拔掉 -> 防水 -> 好友 -> 關閉

        CurrentCallStatus = self._getCallStatus()

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append(Command.Ctrl_U)
        CmdList.append('p')

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                [
                    i18n.SetCallStatus,
                    i18n.Success
                ],
                Screens.Target.InUserList,
                BreakDetect=True
            )
        ]

        while CurrentCallStatus != inputCallStatus:
            self._ConnectCore.send(
                Cmd,
                TargetList,
                ScreenTimeout=Config.ScreenLongTimeOut
            )

            CurrentCallStatus = self._getCallStatus()

    def giveMoney(self, ID, Money):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if self._UnregisteredUser:
            raise Exceptions.UnregisteredUser(Util.getCurrentFuncName())

        if not isinstance(ID, str):
            raise TypeError(Log.merge([
                'ID',
                i18n.MustBe,
                i18n.String
            ]))

        if not isinstance(Money, int):
            raise TypeError(Log.merge([
                'Money',
                i18n.MustBe,
                i18n.Integer
            ]))

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('P')
        CmdList.append(Command.Enter)
        CmdList.append('P')
        CmdList.append(Command.Enter)
        CmdList.append('O')
        CmdList.append(Command.Enter)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                i18n.NoMoney,
                '你沒有那麼多Ptt幣喔!',
                BreakDetect=True,
                Exceptions=Exceptions.NoMoney
            ),
            ConnectCore.TargetUnit(
                i18n.NoMoney,
                '金額過少，交易取消!',
                BreakDetect=True,
                Exceptions=Exceptions.MoneyTooFew
            ),
            ConnectCore.TargetUnit(
                i18n.NoMoney,
                '交易取消!',
                BreakDetect=True,
                Exceptions=Exceptions.UnknowError
            ),
            ConnectCore.TargetUnit(
                [
                    i18n.Transaction,
                    i18n.Success
                ],
                '按任意鍵繼續',
                BreakDetect=True
            ),
            ConnectCore.TargetUnit(
                i18n.ConstantRedBag,
                '要修改紅包袋嗎',
                Response=Command.Enter
            ),
            ConnectCore.TargetUnit(
                i18n.VerifyID,
                '完成交易前要重新確認您的身份',
                Response=self._Password + Command.Enter
            ),
            ConnectCore.TargetUnit(
                i18n.InputMoney,
                '要給他多少Ptt幣呢?',
                Response=Command.Tab + str(Money) + Command.Enter
            ),
            ConnectCore.TargetUnit(
                i18n.InputID,
                '這位幸運兒的id',
                Response=ID + Command.Enter
            ),
            ConnectCore.TargetUnit(
                i18n.AuthenticationHasNotExpired,
                '認證尚未過期',
                Response='y' + Command.Enter
            ),
            ConnectCore.TargetUnit(
                i18n.TradingInProgress,
                '交易正在進行中',
                Response=Command.Space
            )
        ]

        self._ConnectCore.send(
            Cmd,
            TargetList,
            ScreenTimeout=Config.ScreenLongTimeOut
        )

    def mail(
        self,
        ID: str,
        Title: str,
        Content: str,
        SignFile
    ):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        if not isinstance(ID, str):
            raise TypeError(Log.merge([
                'ID',
                i18n.MustBe,
                i18n.String
            ]))

        if not isinstance(Title, str):
            raise TypeError(Log.merge([
                'Title',
                i18n.MustBe,
                i18n.String
            ]))

        if not isinstance(Content, str):
            raise TypeError(Log.merge([
                'Content',
                i18n.MustBe,
                i18n.String
            ]))

        CheckSignFile = False
        for i in range(0, 10):
            if str(i) == SignFile or i == SignFile:
                CheckSignFile = True
                break

        if not CheckSignFile:
            SignFile = SignFile.lower()
            if SignFile != 'x':
                raise ValueError(Log.merge([
                    'SignFile',
                    i18n.ErrorParameter,
                    SignFile
                ]))

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('M')
        CmdList.append(Command.Enter)
        CmdList.append('S')
        CmdList.append(Command.Enter)
        CmdList.append(ID)
        CmdList.append(Command.Enter)

        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                [
                    i18n.Start,
                    i18n.SendMail
                ],
                '主題：',
                BreakDetect=True
            ),
            ConnectCore.TargetUnit(
                i18n.NoSuchUser,
                '【電子郵件】',
                Exceptions=Exceptions.NoSuchUser(ID)
            ),
        ]

        self._ConnectCore.send(
            Cmd,
            TargetList,
            ScreenTimeout=Config.ScreenLongTimeOut
        )

        CmdList = []
        CmdList.append(Title)
        CmdList.append(Command.Enter)
        CmdList.append(Content)
        CmdList.append(Command.Ctrl_X)

        Cmd = ''.join(CmdList)

        if SignFile == 0:
            SingFileSelection = i18n.NoSignatureFile
        else:
            SingFileSelection = i18n.Select + ' ' + \
                str(SignFile) + 'th ' + i18n.SignatureFile

        TargetList = [
            ConnectCore.TargetUnit(
                i18n.AnyKeyContinue,
                '任意鍵',
                BreakDetect=True
            ),
            ConnectCore.TargetUnit(
                i18n.SaveFile,
                '確定要儲存檔案嗎',
                Response='s' + Command.Enter,
                # Refresh=False,
            ),
            ConnectCore.TargetUnit(
                i18n.SelfSaveDraft,
                '是否自存底稿',
                Response='y' + Command.Enter
            ),
            ConnectCore.TargetUnit(
                SingFileSelection,
                '選擇簽名檔',
                Response=str(SignFile) + Command.Enter
            ),
            ConnectCore.TargetUnit(
                SingFileSelection,
                'x=隨機',
                Response=str(SignFile) + Command.Enter
            ),
        ]

        self._ConnectCore.send(
            Cmd,
            TargetList,
            ScreenTimeout=Config.ScreenLongTimeOut
        )

        Log.showValue(
            Log.Level.INFO,
            i18n.SendMail,
            i18n.Success
        )

    def hasNewMail(self):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('M')
        CmdList.append(Command.Enter)
        CmdList.append('R')
        CmdList.append(Command.Enter)
        CmdList.append('1')
        CmdList.append(Command.Enter)
        CmdList.append('$')
        Cmd = ''.join(CmdList)

        #
        TargetList = [
            ConnectCore.TargetUnit(
                i18n.MailBox,
                Screens.Target.InMailBox,
                BreakDetect=True
            )
        ]

        self._ConnectCore.send(
            Cmd,
            TargetList,
            ScreenTimeout=Config.ScreenLongTimeOut
        )

        OriScreen = self._ConnectCore.getScreenQueue()[-1]

        pattern = re.findall('[\s]+[\d]+ (\+)[\s]+', OriScreen)
        return len(pattern)

    def getBoardList(self):
        self._OneThread()

        if not self._LoginStatus:
            raise Exceptions.RequireLogin(i18n.RequireLogin)

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('F')
        CmdList.append(Command.Enter)
        CmdList.append('y')
        CmdList.append('$')
        Cmd = ''.join(CmdList)

        TargetList = [
            ConnectCore.TargetUnit(
                i18n.BoardList,
                Screens.Target.InBoardList,
                BreakDetect=True
            )
        ]

        self._ConnectCore.send(
            Cmd,
            TargetList,
            ScreenTimeout=Config.ScreenLongTimeOut
        )
        OriScreen = self._ConnectCore.getScreenQueue()[-1]

        MaxNo = 0

        for line in OriScreen.split('\n'):
            if '◎' not in line:
                continue

            if line.startswith(self._Cursor):
                line = line[len(self._Cursor):]

            # print(f'->{line}<')

            FrontPart = line[:line.find('◎')]
            FrontPartList = [x for x in FrontPart.split(' ')]
            FrontPartList = list(filter(None, FrontPartList))
            # print(f'FrontPartList =>{FrontPartList}<=')
            MaxNo = int(FrontPartList[0])

        Log.showValue(
            Log.Level.DEBUG,
            'MaxNo',
            MaxNo
        )

        if Config.LogLevel == Log.Level.INFO:
            PB = progressbar.ProgressBar(
                max_value=MaxNo,
                redirect_stdout=True
            )

        CmdList = []
        CmdList.append(Command.GoMainMenu)
        CmdList.append('F')
        CmdList.append(Command.Enter)
        CmdList.append('y')
        CmdList.append('0')
        Cmd = ''.join(CmdList)

        BoardList = []
        while True:

            self._ConnectCore.send(
                Cmd,
                TargetList,
                ScreenTimeout=Config.ScreenLongTimeOut
            )

            OriScreen = self._ConnectCore.getScreenQueue()[-1]
            # print(OriScreen)
            for line in OriScreen.split('\n'):
                if '◎' not in line:
                    continue

                if line.startswith(self._Cursor):
                    line = line[len(self._Cursor):]

                # print(f'->{line}<')

                FrontPart = line[:line.find('◎')]
                FrontPartList = [x for x in FrontPart.split(' ')]
                FrontPartList = list(filter(None, FrontPartList))
                # print(f'FrontPartList =>{FrontPartList}<=')
                No = int(FrontPartList[0])
                # print(f'No =>{No}<=')
                # print(f'LastNo =>{LastNo}<=')

                Log.showValue(
                    Log.Level.DEBUG,
                    'Board NO',
                    No
                )

                BoardName = FrontPartList[1]
                if BoardName.startswith('ˇ'):
                    BoardName = BoardName[1:]

                Log.showValue(
                    Log.Level.DEBUG,
                    'Board Name',
                    BoardName
                )

                BoardList.append(BoardName)

                if Config.LogLevel == Log.Level.INFO:
                    PB.update(No)

            if No == MaxNo:
                break
            Cmd = Command.Ctrl_F

        if Config.LogLevel == Log.Level.INFO:
            PB.finish()

        return BoardList


if __name__ == '__main__':

    print('PTT Library v ' + Version)
    print('Developed by PTT CodingMan')
