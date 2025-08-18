/// @attension ゲームショウ用の処理は IsTGSMode でのみ分岐しています

#include "CommonTypes.h"
#include "CommonTypes.inner.h"
#include "ui_common_const.h"
#include "utility.h"
#include "locale.h"

BG					g_bg = BG();
BG					g_main_frame = BG();
Fade				g_fade = Fade();
Resource			g_resource = Resource();
Chat				g_chat = Chat();
UI					g_prev_object;
bool g_is_mission_clear = false; // 直前のミッションをクリアしたか？

int		g_music_fadetime = 60;
Music	g_music = Music();

// モードセレクト後のデータロード処理
bool	LoadSaveData_ModeSelect()
{
	WaitSaveLoad();
	ModeSelectLoadSaveData();
	WaitSaveLoad();
	return IsCompleteSaveLoad();
}

// タイトルに戻る際のセーブ
void	SaveAllData_ReturnTitle(bool is_focus)
{
	WaitSaveLoad();
	Save(is_focus, "Contents_AutoSaveRetry_ReturnTitle",true);
}

void CheckUnlockArmorWeaponLimit()
{
	int clear_ratio = GetAchivementValue_Int("AllClearRatio");
	if( clear_ratio >= 7000 ) {
		if( UnlockArmorWeaponLimit() ) {
			Dialog_Message( "Sys_UnlockArmorWeaponLimit" );
		}
	}
}

//-- ----------------------------------------------------------------------------------------------
int main()
{
	// 起動直後アクティビティ－はすべて無効化
	if( IsPs5() ){
		ps5_UnavailableAllActivities(); 
	}

	SetMemoryType(1);

	string current_routine = "Boot"; // 最初にコルーチン呼び出しを行う関数を登録しておく

	DeleteAllMenuUi();

	if( GetStartupRoutine().length() > 0 ) {
		print( "[" + GetStartupRoutine() + "] changed" );
		current_routine = GetStartupRoutine();
	}

	while( true ) {
		// 正式な呼び出し型情報を作成する
		string exec = "string " + current_routine + "()";
		print(exec);
		// コルーチン呼び出し
		coRoutine routine = createCoRoutine(exec);
		// コルーチンが完了するまで待つ
		routine.wait();
		// コルーチンから戻り値を取り出す
		current_routine = routine.resultString();

		// exitであれば抜ける
		if( "exit" == current_routine ) {
			break;
		}
	}

	InitializeAll();

	print("MainScript2 end");
	return 0;
}

//===============================================================================
// 起動
string Boot()
{
	// 起動時、セーブデータ引き継ぎ前や、ReBoot呼び出し時など、アクティビティー無効化
	if( IsPs5() ){
		ps5_UnavailableAllActivities(); 
	}

	Network_SetLocation(BOOTING);

	WaitJob();
	Reset( RESET_FLAG_ALL );

	//#if defined(_PC_VER_) // マウスポインティングUI対応
	if( IsPC() ){
		g_resource.CreateMouseCursor();
	}
	//#endif // defined(_PC_VER_)

	if( IsPs5() ){
        ps5_ConvertSaveDataFromPs4();
    }

	if( IsPs5() ){
		if( ps5_isActivityBoot() ){
			return "ActivityBoot";
		}
	}
	if( INVITATION_TYPE_NONE != GetInvitationType() ){
		return "Invite";
	}

	return "StartToTitle";
}

//===============================================================================
//PS4セーブデータ移行処理
void ps5_ConvertSaveDataFromPs4(){
	ps5_serchTransDir();
	WaitJob();

    if(ps5_isValidTransDir() == true){

		// PS4版EDF6のセーブデータがあります。引き継ぎますか？
		if(DIALOG_YES == Dialog_YesNo("TransferSaveDataFromPS4_Comfirm"))
		{
			// 移行処理を実行するか
			bool isTransExcute = true;

			while(true)
			{
				if(isTransExcute)
				{
					ps5_ImportPs4SaveData();
					WaitJob();
				}
				else
				{
					Wait(1);
				}


				int ret = ps5_isFinishTransFromPs4();
				switch(ret)
				{
					// まだ終わっていない
					case TRANS_IN_PROGRESS:
						isTransExcute = false;
					    continue;

					// エラーが解消されたのでもう一度実行する
					case TRANS_COMPLETED_WITH_ERROR:
						isTransExcute = true;
						continue;

					// 全部がエラーなしでジョブが完了
					case TRANS_COMPLETED_WITH_NO_ERROR:
					    Dialog_Message("TransferSaveDataFromPS4_Done");
						break;

					// 一つでも引継ぎ不可能なファイルが存在した場合
					case TRANS_COMPLETED_WITH_FAILURE:
						Dialog_Message("TransferSaveDataFromPS4_Failure");
						break;
				}

				break;

			}
		}
    }
}


//===============================================================================
// 再起動
string ReBoot()
{
	// 起動時、セーブデータ引き継ぎ前や、ReBoot呼び出し時など、アクティビティー無効化
	if( IsPs5() ){
		ps5_UnavailableAllActivities(); 
	}

	Network_SetLocation(BOOTING);

	g_music.Stop( 1 );
	// ジョブのコールバック等が仕掛けられている可能性があるので、ジョブの終了を待つ
	WaitJob();

	g_music.WaitStop();

	// 完全リセット
	// マップ、UI、リソースの解放、サウンドの停止、ネットワークの停止等、システム系のリセットが行われる
	// ゲームの進行状況は別途 Reset を呼び出す
	SystemReset();

	return "Boot";
}

void InitializeAll()
{
	// リソース開放
	g_resource.FreeGroup(RESOURCE_GROUP_SCENE);
	g_resource.FreeGroup(RESOURCE_GROUP_MODE);

	// ネットワークコード終了
	Network_End();

	// 戻ってきた時のセーブロード待ち
	WaitSaveLoad();

	// UIを全部掃除
	DeleteAllMenuUi();

	//
	Reset( RESET_FLAG_ALL );

	//
	ResetControllerAssign();	// プレイヤーを一人に設定

	//フェード用のUI作成
	g_fade.Create();

	// スクリプト起動時のリソース常駐を行う
	g_resource.Entry("app:/UI/UiResourceGroup_BootScript.sgo", SYSTEM_GROUP_TITLE, 0);
	g_resource.Wait();

}

//===============================================================================
// 招待処理
//  とりあえず失敗したらTitleに戻している
string Invite()
{
	g_music.Stop(g_music_fadetime);
	g_fade.Wait(); // 事前にFadeout呼び出しがあれば同期、なければ何もしない
	g_music.WaitStop();

	//初期化
	InitializeAll();

	Network_SetLocation(BOOT_COMPLETE);

	titleSaveDataLoad(true);

	// PlayGoチェック
	if( false == IsDownloadComplete() ) {
		Invitation_Cancel();
		g_fade.Wait();
		g_fade.Transparency();
		Dialog_Message( "PlayGoDownload_Invitation" );
		return "StartToTitle";
	}

	g_resource.Entry("app:/UI/UiResourceGroup_SlotSel.sgo", SYSTEM_GROUP_SCENE, 0);

	g_music.Play( "BGM_E4S01_TitleGamen" );			// BGM:タイトル画面

	g_fade.Wait();
	g_fade.Transparency();

	if ( !IsEpic() ) { 
	WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ
	}
	WaitSaveLoad();

	if( IsCompleteSaveLoad() == false ) {
		Invitation_Cancel();
		Dialog_Message( "Sys_LoadFailed_ToTitle" );
		return "StartToTitle";
	}

	// オンラインモードへの接続を行う
	Signin @signin = Signin();

	// 各プラットフォームで必要なサインイン作業を行う
	while( true ) {
		InvokeResult result = signin.PlatformSignin();
		if( !result.IsSuccess() ) {
			if( DIALOG_YES == Dialog_YesNo( "GameMode_OnlineFailed" ) ) {
				return "StartToTitle";
			}
			continue;
		}
		break;
	}

	// 招待先のセッション情報を取得する
	InvitationReceive invite;
	if( false == invite.Wait() ) {
		Invitation_Cancel();
		Dialog_Message( "GameMode_OnlineFailed" );
		return "StartToTitle";
	}

	if ( IsPC() ) { 
	WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ
	}


	g_fade.Black(); // 画面は黒で開始

	g_bg.Play("app:/ui/lyt_SlotSelect_BG.sgo");
	g_main_frame.Play("app:/ui/lyt_SlotFrame.sgo");
	g_main_frame.GetObject().SetDrawOrder(g_fade.GetObject());

	// スロット選択
	UI object = CreateSlotSelectUi2(UISLOTSELECT_INVITATION);
	g_fade.In();

	object.WaitCloseRequest();

	if( GetUiExitCode() != Hui_ReturnOK) {
		Invitation_Cancel();
		return "StartToTitle";
	}

	int invitation_type = GetInvitationType();

	int mode;
	if( INVITATION_TYPE_INVITE == invitation_type ) {
		// 招待された側のみパッケージチェックを行う
		mode = GetInvitationMode();
		// パッケージを持っているかチェック
		if( mode < 0 ) {
			Invitation_Cancel();
			// Sys_InviteCancel
			Dialog_Message( "Sys_JoinGameCancel" );

			return "StartToTitle";
		}
	} else {
		// テスト用経路、boot経由での本番では利用されない
		mode = GetModeNo(GAME_ONLINE_SCENARIO,0);
	}
	WaitSaveLoad();

	// 招待状に設定されているモードに設定
	FreeResourceGroup( RESOURCE_GROUP_MODE );
	if( !SetMode(mode) ) {
		Invitation_Cancel();
		Dialog_Message( "Lobby_NotHaveContents" );
		return "StartToTitle";
	}

	// モード、ゲームデータ読み込み
	if( LoadSaveData_ModeSelect() == false ){
		Invitation_Cancel();
		// エラーがあったのでスロットセレクトに
		Dialog_Message( "Sys_LoadFailed_ToTitle" );
		return "StartToTitle";
	}
	UnlockDownloadContents();

	UpdateAchievementCounter( false, false );
	AchievementAddCount("PlayCount");

	DeleteAllMenuUi();

	return "OnlineMode";
}


//===============================================================================
// アクティビティによる起動
string ActivityBoot()
{
	g_music.Stop(g_music_fadetime);
	g_fade.Wait(); // 事前にFadeout呼び出しがあれば同期、なければ何もしない
	g_music.WaitStop();

	//初期化
	InitializeAll();

	Network_SetLocation(BOOT_COMPLETE);

	g_fade.Wait();
	g_fade.Transparency();
	titleSaveDataLoad(true);

	WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ
	WaitSaveLoad();

	if( IsCompleteSaveLoad() == false ) {
		Dialog_Message( "Sys_LoadFailed_ToTitle" );
		return "StartToTitle";
	}

	g_resource.Entry("app:/UI/UiResourceGroup_ModeSel.sgo", SYSTEM_GROUP_SCENE, 0);

	//
	// TODO: 対応するスロットのデータをロードする
	// 失敗したらタイトルへ戻す
	//
	if( AutoLoad_LastSave() == false ){
		Dialog_Message( "Sys_LoadFailed_ToTitle" );
		return "StartToTitle";
	}

	// オンラインモードへの接続を行う（ActivityBootが呼ばれない想定なので無効）
	//if ( IsPC() ) {
	//	Signin @signin = Signin();
	//
	//	// 各プラットフォームで必要なサインイン作業を行う
	//	while( true ) {
	//		InvokeResult result = signin.PlatformSignin();
	//		if ( IsSteam() ) {
	//			break; // Steam版は気にせず先に進む
	//		}
	//		if( !result.IsSuccess() ) {
	//			Dialog_Message( "CONNECT_EOS_FAILED" ) ) {
	//			return "StartToTitle";
	//		}
	//		break;
	//	}
	//}

	g_resource.Wait();

	//通常時はタイトル画面に再生命令があり、このままでは無音のまま進行してしまう為、ここで再生開始
	g_music.Play( "BGM_E4S01_TitleGamen" );			// BGM:タイトル画面

	// TODO: セーブスロットを確定できると仮定して「モード選択」へ遷移
	// スロットの確定ができない場合はセーブスロット選択へ遷移でも良い
	//（どちらも作成基準上の問題が無いか確認が必要）
	return "ModeSelect";
}


//===============================================================================
//タイトル開始まで
string StartToTitle()
{
	// タイトルに戻る時点で、アクティビティーを無効化
	if( IsPs5() ){
		ps5_UnavailableAllActivities(); 
	}

	Invitation_Clear();

	g_music.Stop(g_music_fadetime);

	g_fade.Wait(); // 事前にFadeout呼び出しがあれば同期、なければ何もしない
	g_fade.Black(); // 画面は黒で開始

	g_music.WaitStop();

	//初期化
	InitializeAll();

    //システムコンフィグと言語設定を読み込み
	LoadSystemSaveData();
	WaitSaveLoad();

	// 企業ロゴ表示
	CompanyLogo();

	g_fade.Wait();
	g_fade.Transparency();
	Network_SetLocation(BOOT_COMPLETE);

	// 招待が届いているので、タイトル画面への移行をしないようにする
	WaitInvitationNewSignal();

	g_fade.Black();

	// タイトル表示
	Title();

	if( IsTGSMode() ) {
		return "HQMain";
	}
	return "SlotSelect";
}



class Logo {
	UI m_handle;
	string m_current;

	int play(string file,bool is_button_skipable) {
		m_current = file;

		if( false == IsLogoDisplayable(m_current) ) {
			return 0;
		}

		bool is_movie = (-1 != file.findLast(".MP4") );

		if( false == is_movie ) {
			string arg = "[tex_path|";
			arg += file;
			arg += "]";
			arg += "[skippable|";
			if ( is_button_skipable==true)
			{	arg += "true";		}
			else
			{	arg += "false";		}
			arg += "]";
			m_handle = CreateUiFileOpt("app:/ui/lyt_Logo_sandlot.sgo",arg);
			g_fade.In();
		} else {
			m_handle = PlayLogoMovie("APP:/UI/"+file,is_button_skipable);
		}

		return 1;
	}
	void wait(){
		m_handle.WaitClose();
		g_fade.Wait();

		SetLogoDisplayed(m_current);
		m_current = "";
	}
};

//-----------------------------
// 企業ロゴ
void CompanyLogo()
{
	g_resource.Entry("app:/UI/UiResourceGroup_CompanyLogo.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.Wait();

	// demonized: Skip all intro by commenting logo functions
	// Logo logo = Logo();

    // int locale = GetLocale();
    // if( locale == ASIA ){
    //     logo.play("CLE_LOGO.MP4",true);
    //     logo.wait();
    // }

	// logo.play("LOGO_D3P.DDS",true);
	// logo.wait();

	// logo.play("LOGO_CRIWARE.DDS",true);
	// logo.wait();

	// logo.play("LOGO_HAVOK.DDS",true);
	// logo.wait();

	// if( ps5_isNoticeScreenSkip() == false){
	// 	logo.play("LOGO_SANDLOT.DDS",true);
	// 	logo.wait();
	// }

	g_fade.Out();
	g_fade.Wait();

	// ロゴ表示で使用されたリソースを開放
	g_resource.FreeGroup(SYSTEM_GROUP_SCENE);
}

void LoadSystemSaveData(){
	// tgsモードはロードは行わない
	if( false == IsTGSMode() ) {
		TitleLoadSaveData(true);	// システムコンフィグとスロット選択用データロード開始
	}
	WaitSaveLoad();	// ロード完了待ち
}

void titleSaveDataLoad(bool is_langsavedataload)
{
	WaitSaveLoad();	// 戻ってくる際のセーブ処理待機

	if ( !IsEpic() ||  IsDoneSigninSingleton() ) { // PC版はサインインするまでスキップ
		SearchUpdateAddon();	//追加コンテンツの更新開始
	}

	// tgsモードはロードは行わない
	if( false == IsTGSMode() ) {
		TitleLoadSaveData(is_langsavedataload);	// システムコンフィグとスロット選択用データロード開始
	}
}

//-----------------------------
// タイトル画面
void Title()
{
	//リソース読み込み
	g_resource.Entry("app:/UI/UiResourceGroup_Title.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.Wait();

	g_bg.Play("app:/ui/lyt_TitleBg.sgo");
	g_music.Play( "BGM_E4S01_TitleGamen" );			// BGM:タイトル画面

	g_fade.In();

	UI ui_title = CreateUiFile("app:/ui/lyt_Title.sgo");

	//次の画面のリソース読み込み開始
	g_resource.Entry("app:/UI/UiResourceGroup_SlotSel.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.Entry("app:/UI/UiResourceGroup_ModeSel.sgo", SYSTEM_GROUP_SCENE, 0);

	titleSaveDataLoad(false);

	//if ( IsEpic() ) {
	//	
	//}

	g_fade.Wait();

	if ( IsPC() ) {
		// 各プラットフォームで必要なサインイン作業を行う
		if ( IsDoneSigninSingleton() ) {
			ui_title.PostMessage("EpicSigninSuccess", "[result|true]");
		} else {
			while( true ) {
				// ログイン中テキストに書き換え
				if ( IsEpic() ) {
					ui_title.SetCompnentText("PushButtonText","CONNECT_EPIC_ONLINE_SERVICE");
				}
				InvokeResult result = PlatformSigninSingleton();
				if ( IsSteam() ) {
					break; // Steam版は気にせず先に進む
				}
				if( !result.IsSuccess() ) {
					Dialog_Message( "CONNECT_EOS_FAILED" );
					continue;
				}
				if ( IsEpic() ) {
					// テキストを元に戻す
					ui_title.SetCompnentText("PushButtonText","PadAssign_PushStart");
					ui_title.PostMessage("EpicSigninSuccess", "[result|true]");
				}
				break;
			}
		}
	}

	if ( IsPC() ) {
		if ( IsDoneSigninSingleton() ) {
			ConnectSingleton();
			
			if ( IsEpic() )//接続出来たら所有権の確認
			{
				InvokeResult result = CheckOwnerShipSingleton();
				if( !result.IsSuccess() )
				{
					while( true ) {
						Dialog_Message( "EPIC_OWNERSHIP_FAILED" );
						ExitApp();
					}
				}
				
				WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ
				SearchUpdateAddon();	//追加コンテンツの更新開始
			}
		}
	}

	ui_title.WaitClose();
	WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ


	g_resource.Wait();
	// ロード終了待機
	WaitSaveLoad();
	if( IsCompleteSaveLoad() == false )
	{
		// ここでのロードは停止しない(エラーはロード処理中で表示)
	}

	// 次の画面へ
	g_fade.Out();
	g_fade.Wait();
	g_bg.Stop();
}

//===============================================================================
// ゲームショウのゲーム終了後画面
string TSGEnding()
{
	g_resource.Entry("app:/UI/UiResourceGroup_TGSEnding.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.Wait();
	g_bg.Play("app:/ui/lyt_TGS2016_END.sgo");

	//Dialog_Message("Sys_PressButton");
	UI tgs = CreateUiFile("app:/ui/lyt_TgsEnd.sgo");
	g_fade.In();
	tgs.WaitClose();	//uiが

	g_fade.Out();
	g_fade.Wait();

	g_bg.Stop();

	return "Boot";
}

//===============================================================================
// スロット選択
string SlotSelect()
{
	// ゲームモード選択画面から戻るで遷移した場合が考えられるので、アクティビティーを無効化
	if( IsPs5() ){
		ps5_UnavailableAllActivities(); 
	}

	Reset( RESET_FLAG_SLOT_RESET );
	g_bg.Play("app:/ui/lyt_SlotSelect_BG.sgo");
	g_main_frame.Play("app:/ui/lyt_SlotFrame.sgo");
	g_main_frame.GetObject().SetDrawOrder(g_fade.GetObject());

	UI object = CreateSlotSelectUi2(UISLOTSELECT_NORMAL);
	object.SetDrawOrder(g_prev_object);
	g_fade.In();

	object.WaitCloseRequest();

	string ret_string;
	if( GetUiExitCode() == Hui_ReturnOK)
	{
		ret_string = "ModeSelect";
	}
	else
	{
		g_fade.Out();
		ret_string = "StartToTitle";
	}
	return ret_string;
}

//===============================================================================
// ゲームモード選択画面に入った時用のモードダミー設定入りのアクティビティ更新処理
// モード設定が初期化されるので、モード設定の初期化時以外で使用しない
void    ps5_UpdateActivity_ModeSelect()
{
	//アクティビティ情報を反映する為、モードを仮決定し情報を読み込む
	if( IsPs5() ){
		Reset( RESET_FLAG_MODE_RESET );
		if( SetMode( GetModeNo(GAME_OFFLINE_SCENARIO,0)) ) {
			LoadSaveData_ModeSelect();
			//ModeSelectLoadSaveData完了時に、アクティビティが反映される
		}
		//仮決定した情報を破棄する
		Reset( RESET_FLAG_MODE_RESET );
	}
}
//===============================================================================
// モード選択
string ModeSelect()
{
	ps5_UpdateActivity_ModeSelect();

	Reset( RESET_FLAG_MODE_RESET );

	g_fade.In();

	g_bg.Play("app:/ui/lyt_SlotSelect_BG.sgo");
	g_main_frame.Play("app:/ui/lyt_SlotFrame.sgo");
	g_main_frame.GetObject().SetDrawOrder(g_fade.GetObject());

	UI ui_handle = CreateUiFile("app:/ui/lyt_ModeSelect.sgo");
	g_prev_object = ui_handle;
	ui_handle.WaitCloseRequest();

	//キャンセルならもどる
	int exit_code = GetUiExitCode();
	if( exit_code ==  Hui_ReturnCancel)
	{
		return "SlotSelect";	//戻る
	}

	g_resource.FreeGroup(RESOURCE_GROUP_MODE);

	// 返値によりモードを切り替え
	int mode_id = ((exit_code & 0xff00) >> 8);	// GameModeID
	int mode_no = ( exit_code & 0x00ff); 			// pkgの順

	if( mode_id == UIMODESELECT_RESULT_CANCEL ) {
		return "SlotSelect";
	}

	// モード設定

	string return_jmp = "StartToTitle";

	if( UIMODEINDEX_ERROR != mode_no ) {
		switch( mode_id ) {
		case GAME_OFFLINE_SCENARIO:
			return_jmp = "HQMain";
			break;
		case GAME_ONLINE_SCENARIO:
			return_jmp = "OnlineMode";
			break;
		}

		SetMode(mode_no);

		// モード、ゲームデータ読み込み
		if( LoadSaveData_ModeSelect() == false ){
			// エラーがあったのでスロットセレクトに
			Dialog_Message( "Sys_LoadFailed_ToSlotSelect" );

			g_prev_object = UI();
			return "SlotSelect";
		}
		UnlockDownloadContents();
		UpdateAchievementCounter( false, false );
		AchievementAddCount("PlayCount");
	}

	g_music.Stop(g_music_fadetime);

	g_fade.Out();
	g_fade.Wait();

	DeleteAllMenuUi();
	g_fade.Black();

	Opening();

	return return_jmp;
}

//===============================================================================
// オープニング(新規スロットデータ開始時に一度だけ表示するストーリーテキスト)
void Opening()
{
	if( GetContentID() != 0 )
	{
	    return; // ミッションパック時には表示しない
	}

	if( IsShowedOpening() )
	{
		return;
	}

	g_music.WaitStop();
	g_fade.In();

	// demonized: disable opening playback 
	// PlayOpening();
	
	Save(false, "Contents_AutoSaveRetry_Opening",true);	// セーブ開始
}


//===============================================================================
// 作戦司令本部画面
string HQMain()
{
	g_resource.Entry("app:/ui/UiResourceGroup_HQ.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.EntryModeImage(0);
	g_resource.Wait();

	g_fade.Wait();

	g_bg.Play("app:/ui/lyt_bg.sgo");
	g_main_frame.Play("app:/ui/lyt_MainFrame.sgo");
	g_main_frame.GetObject().SetDrawOrder(g_fade.GetObject());

	g_music.PlaySelectedMissionBGM_Start();   // 現在のミッションに設定されたBGMを再生する


	if ( IsEpic() || IsDoneConnectSingleton() )
	{
		{
			if( !IsNowConnectSingleton() )
			{
				InvokeResult result = PlatformSigninSingleton();
				if( result.IsSuccess() )
				{
					ConnectSingleton();
				}
				
				if( !IsNowConnectSingleton() )
				{
					g_fade.Wait();
					g_fade.In();
					
					if( false == IsTGSMode() )
					{
						SaveAllData_ReturnTitle(true);
					}
					
					g_fade.Wait();
					
					Dialog_Message( "CONNECT_EOS_FAILED" );
					return "StartToTitle";
				}
				
				result = CheckOwnerShipSingleton();
				if( !result.IsSuccess() )
				{
					g_fade.Wait();
					g_fade.In();
					while( true ) {
						Dialog_Message( "EPIC_OWNERSHIP_FAILED" );
						ExitApp();
					}
				}
			}
		}
	}
	
	UI ui_handle3D = CreateUiFile("app:/ui/lyt_HUiHQ3DModel.sgo");

	UI ui_handle = CreateUiFile("app:/ui/lyt_HUiHQMain.sgo");

	//-- フェードイン
	g_fade.In();
	g_fade.Wait();

	//-- UI操作終了 --
	ui_handle.WaitCloseRequest();
	g_music.Stop( g_music_fadetime );
	//
	if( GetUiExitCode() ==  Hui_ReturnOK)
	{
		//ミッションへ
		g_fade.Out();
		g_fade.Wait();

		return "PlayMission_Offline";
	}

	//タイトルに戻るに設定された
	if( false == IsTGSMode() && GetUiExitCode() ==  Hui_HQMain_Return_GotoTitle)
	{
		SaveAllData_ReturnTitle(true);
	}

	//タイトルに戻る
	g_fade.Out();
	g_fade.Wait();

	ui_handle3D.Close();

	g_music.WaitStop();

	return "StartToTitle";	//todo:
}

//===============================================================================
// ミッション共通処理
int PlayMission_Common()
{
	g_fade.Out();
	g_fade.Wait();
	DeleteAllMenuUi();

	g_resource.FreeGroup(RESOURCE_GROUP_SCENE);

	g_resource.Entry("app:/ui/UiResourceGroup_InMission.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.EntryLoadinImage(0);

	SoldierTypeSortieAddCount();	// 兵科ごとの出撃回数カウントアップ

	// ネットワークの現在位置を更新する(エラー表示用)
	Network_SetLocation(GAME_LOADING);

	// ホスト側のモード番号をチェックして正しいモードでなれけばモード切替を行う

	MissionSync sync("PreSync");
	if( !sync.Wait() ) {
		Dialog_Message("Online_Game_Disconnect");

		g_fade.Black();
		/// 通信に失敗したので、ロビーへ戻されます
		/// 切断済みになっていますが、GAME_LOADINGなのでメッセージの表示が必要です。
		return MISSION_RESULT_LOBBY;
	}

	if( !IsGameHost() ) {
		// ホスト以外はＤＬＣ切替えが終わっていない可能性があるので、ここで復旧させる
		if( false == ApplyModeNo(sync.GetNewMode()) ) {
			return MISSION_RESULT_RETURNTITLE;
		}
	}

	sync = MissionSync("Sync");
	if( !sync.Wait() ) {
		Dialog_Message("Online_Game_Disconnect");

		g_fade.Black();
		/// 通信に失敗したので、ロビーへ戻されます
		/// 切断済みになっていますが、GAME_LOADINGなのでメッセージの表示が必要です。
		return MISSION_RESULT_LOBBY;
	}

	// ホスト側のモード番号をチェックして正しいモードでなれけばモード切替を行う


	SetUsedWeapon();
	ResetResult();				// アイテムの取得状態を完全にリセット
	SetMissionRetryFlag(false);

	int result;

	Match_Start();

	g_resource.Wait();

	SetMemoryType(2);
	for(;;){
		// ネットワークのゲームセッションをリセットする(ローカルの状態をリセットする)
		Network_Session_Reset();

		result = Mission();
		if( result != MISSION_RESULT_RETRY) break;
		SetMissionRetryFlag(true);
	}
	// ゲームシーン開放
	g_resource.FreeGroup(RESOURCE_GROUP_SCENE);

	SetMemoryType(1);

	Match_End(result);

	//フェード用のUI再作成
	g_fade.Black();

	switch( result ) {
	case MISSION_RESULT_ABORT:
	case MISSION_RESULT_CLEAR:
		{
			MissionSync sync("Result");
			sync.Wait();
		}
		break;
	}

	// ネットワークのゲームセッションを終了する
	Network_Session_End();

	// ネットワークの現在位置を更新する(エラー表示用)
	Network_SetLocation(MENU_ROOM);

	return result;
}

// オフラインミッションを実行する
string PlayMission_Offline()
{
	if ( IsEpic() || IsDoneConnectSingleton() )
	{
		{
			if( !IsNowConnectSingleton() )
			{
				InvokeResult result = PlatformSigninSingleton();
				if( result.IsSuccess() )
				{
					ConnectSingleton();
				}
				
				if( !IsNowConnectSingleton() )
				{
					g_fade.Wait();
					g_bg.Play("app:/ui/lyt_bg.sgo");
					g_fade.In();
					
					if( false == IsTGSMode() )
					{
						SaveAllData_ReturnTitle(true);
					}
					
					g_fade.Wait();
					
					Dialog_Message( "CONNECT_EOS_FAILED" );
					return "StartToTitle";
				}
				
				result = CheckOwnerShipSingleton();
				if( !result.IsSuccess() )
				{
					g_fade.Wait();
					g_bg.Play("app:/ui/lyt_bg.sgo");
					g_fade.In();
					
					while( true ) {
						Dialog_Message( "EPIC_OWNERSHIP_FAILED" );
						ExitApp();
					}
				}
			}
		}
	}

	AchievementAddCount("OfflinePlayCount");	// オフラインミッション開始回数

	// デモの再生
	g_resource.FreeGroup(RESOURCE_GROUP_SCENE);
	Before();
	g_resource.FreeGroup(RESOURCE_GROUP_SCENE);

	if( false == IsTGSMode() ) {
		g_chat.Rebuild();
	}
	int result = PlayMission_Common();
	g_chat.Release();

	if( MISSION_RESULT_RETURNTITLE == result ) {
		return "StartToTitle";
	}
	if( result == MISSION_RESULT_CLEAR )
	{
		g_is_mission_clear = true;

		if( IsTGSMode() ) {
			return "TSGEnding";
		} else {
			return "Result_Offline";
		}
	}else{
		g_is_mission_clear = false;

		if( IsTGSMode() ) {
			return "TSGEnding";
		} else {
			return "Result_Offline";
			// return "HQMain";
		}
	}
}

//===============================================================================
// オンラインミッション
string PlayMission_Online()
{
	AchievementAddCount("OnlinePlayCount");	// オンラインミッション開始回数

	int result = PlayMission_Common();

	g_is_mission_clear = false;

	if( MISSION_RESULT_RETURNTITLE == result ) {
		return "StartToTitle";
	}

	// ルームとの通信が出来ている場合のみルームに戻す
	if( Network_IsRoomConnected() ) {
		if( result == MISSION_RESULT_CLEAR ){
			g_is_mission_clear = true;
			return "Result_Online";
		}else{
			return "Result_Online";
		}
	} else {
		if( result != MISSION_RESULT_LOBBY ) {
			g_fade.Wait();
			g_fade.Transparency();

			Dialog_Message("Online_Game_Disconnect");

			g_fade.Black();
		}
	}

	g_chat.Release();
	Network_LeaveRoom();

	return "Lobby";
}

void PlayOpening()
{
	UI ui_object = CreateUiFile("app:/ui/lyt_Opening01.sgo");
	g_music.Play("BGM_E6M21_OpTelop");
	ui_object.WaitClose();
}

string OpeningTest()
{
	g_fade.In();
	g_music.Stop( g_music_fadetime );
	g_music.WaitStop();

	// PlayOpening();

	return "";
}

void PlayTutorialOpening()
{
	UI ui_object = CreateUiFile("app:/ui/lyt_Opening02.sgo");
	g_music.Play("BGM_E6M21_OpTelop2");
	ui_object.WaitClose();
}

string TutorialOpeningTest()
{
	g_fade.In();
	g_music.Stop( g_music_fadetime );
	g_music.WaitStop();

	PlayTutorialOpening();

	return "";
}


void PlayEnding(string lyt_sgo,string bgm)
{
	UI object = Ending(lyt_sgo);
	if (object.IsAlive())
	{
		g_music.Play(bgm);
		object.WaitClose();
	}
}

//DLC1エンディング
void DLCEnding1()
{
	UI m_handle = PlayLogoMovie("APP:/UI/EDF6_DLC1Ending_%LOCALE%.mp4",true);
    m_handle.WaitClose();
}

//DLC2エンディング
void DLCEnding2()
{
	UI m_handle = PlayLogoMovie("APP:/UI/EDF6_DLC2Ending_%LANG_AUDIO%.mp4",true);
    m_handle.WaitClose();
}

//===============================================================================
// オフライン用ミッションリザルト
string Result_Offline()
{
	if(  g_is_mission_clear == true ){
		if( IsLastMission()) {
			g_fade.In();
			g_music.Stop( g_music_fadetime );
			g_music.WaitStop();

			if( GetContentID() == 0 ) {
				//エンディング
				PlayEnding("app:/ui/lyt_Ending.sgo","BGM_E6M22_EdTelop");

				//エンドクレジット
				PlayEnding("app:/ui/lyt_EndCredit.sgo","BGM_E6M20_StaffRoll");
			}
			else if( GetContentID() == 1 )
			{
			    DLCEnding1();
			}
            else if( GetContentID() == 2 )
            {
                DLCEnding2();
            }

			g_fade.Out();
		}
	}

	//
	Result_Common( g_is_mission_clear );

	return "HQMain";
}

string EndingTest()
{
	//エンディング
	g_fade.In();
	g_music.Stop( g_music_fadetime );
	g_music.WaitStop();

	//エンディング
	PlayEnding("app:/ui/lyt_Ending.sgo","BGM_E6M22_EdTelop");

	//エンドクレジット
	PlayEnding("app:/ui/lyt_EndCredit.sgo","BGM_E6M20_StaffRoll");

	return "";
}

string EndingOnlineTest()
{
	//エンディング
	g_fade.In();
	g_music.Stop( g_music_fadetime );
	g_music.WaitStop();

	//エンディング
	PlayEnding("app:/ui/lyt_EndingOnline.sgo","BGM_E6M22_EdTelopOnline");

	return "";
}

string DLCEndingTest1()
{
	//エンディング
	g_fade.In();
	g_music.Stop( g_music_fadetime );
	g_music.WaitStop();

	//エンディング
	DLCEnding1();

	return "";
}

string DLCEndingTest2()
{
	//エンディング
	g_fade.In();
	g_music.Stop( g_music_fadetime );
	g_music.WaitStop();

	//エンディング
	DLCEnding2();

	return "";
}

//===============================================================================
// オンライン用ミッションリザルト
string Result_Online()
{
	if(  g_is_mission_clear == true ){
		if( IsLastMission() ) {
			//通常のパッケージの時のみエンディングを呼び出す
			g_fade.In();
			g_music.Stop( g_music_fadetime );
			g_music.WaitStop();

			if( GetContentID() == 0 ) {
				//エンディング
				PlayEnding("app:/ui/lyt_EndingOnline.sgo","BGM_E6M22_EdTelopOnline");
			}
			else if( GetContentID() == 1 )
			{
			    DLCEnding1();
			}
            else if( GetContentID() == 2 )
            {
                DLCEnding2();
            }
			g_fade.Out();
		}
	}

	Result_Common( g_is_mission_clear );

	return "Room";
}

//===============================================================================
// ミッションリザルト画面
void Result_Common(bool is_mission_clear )
{
	DeleteAllMenuUi();	// 念のためUIを掃除
	g_fade.Black();

	g_resource.Entry("app:/ui/UiResourceGroup_Result.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.Wait();

	g_bg.Play("app:/ui/lyt_bg.sgo");
	g_main_frame.Play("app:/ui/lyt_ResultFrame.sgo");
	g_main_frame.GetObject().SetDrawOrder(g_fade.GetObject());

	ResolveResult();	// ドロップアイテムを確定
	UI ui_handle = CreateUiFile("app:/ui/lyt_HUiResult.sgo");
	g_music.PlaySelectedMissionBGM();   // 現在のミッションに設定されたBGMを再生する

	g_fade.In();

	bool is_all_clear = ApplyResult(is_mission_clear );	// ミッション結果を反映
	// クリアしてたら次のミッションへ進める
	if (is_mission_clear  == true)
	{
		ProceedNextMission();   // ApplyResult()より後に呼ぶ。
								// ゲームのミッションは進むがUIが参照するミッション番号はそのまま
	}
	UpdateAchievementCounter( true, is_mission_clear );

	// 武器制限アンロックチェック
	CheckUnlockArmorWeaponLimit();

	// PCリリース版では、他のチートユーザーに巻き込まれ、
	// 自分のセーブがチート後のセーブデータになってしまった場合の回避処置として、
	// セーブ前のデータをバックアップとして保存しておく
	if (IsPC())
	{
		pc_CopySaveSlotToBackupDir();
		pc_WaitCopySaveSlotToBackupDir();
	}

	Save(false, "Contents_AutoSaveRetry",true);	// セーブ開始

	// 次の画面用のプリロード開始
	g_resource.SetSilent(true);
	g_resource.EntryModeImage(0);
	g_resource.SetSilent(false);

	g_fade.Wait();

	// 初めてラストミッションをクリアしたら、全難易度が解放されたことを通知する。
	if (is_all_clear == true)
	{
		Dialog_Message( "NotifyAllMissionClear" );
	}
	ui_handle.WaitCloseRequest();

	// ClearResult();		// ドロップアイテムをクリア
	ResetResult();

	g_fade.Out();
	g_fade.Wait();

	SetUICurrentMission();  // UI の表示ミッションを現在のミッションに合わせる

	DeleteAllMenuUi();
	g_fade.Black();


}

enum OnlineInitializeResult {
	TO_LOBBY,
	TO_ROOM,
	TO_CREATEROOM,
	TO_TITLE,
};

OnlineInitializeResult _OnlineMode()
{
	Signin @signin = Signin();

	InvokeResult result;
	// 各プラットフォームで必要なサインイン作業を行う
	while( true ) {
		result = signin.PlatformSignin();
		if( !result.IsSuccess() ) {
			if( DIALOG_YES == ErrorRetryDialog("GameMode_OnlineFailed",result) ) {
				return TO_TITLE;
			}
			continue;
		}
		break;
	}

	// 接続中待機ウインドウ作成
	UI wait = CreateWaitUi("Online_NameVerify");

	// プラットフォームでオンラインモードを利用してもいいかを確認する
	result = signin.PlatformCheck();
	if( !result.IsSuccess() ) {
		int platform_check = result.GetErrorCode();
		if( NETWORKBEGINRESULT_NO_PLUS == platform_check ) {
			UI object = CreateUiFileOpt("app:/ui/lyt_HUiPsPlus.sgo","");
			object.WaitClose();

			if( 0 != GetUiExitCode() ) {
				// PLUS:成功
				platform_check = SUCCESS;
			} else {
				return TO_TITLE;
			}
		}

		switch( platform_check ) {
		case SUCCESS:
			break;
		case NETWORKBEGINRESULT_NO_SIGNIN:
			ErrorDialog( "GameMode_NoSignin",result );
			return TO_TITLE;
		case FAILED:
			ErrorDialog( "GameMode_OnlineFailed",result );
			return TO_TITLE;
		case NETWORKBEGINRESULT_AGE_RESTRICTION:
		case NETWORKBEGINRESULT_PARENTAL:
			ErrorDialog( "GameMode_OnlineFailed",result );
			return TO_TITLE;
		case NETWORKBEGINRESULT_IRRELEVANT_NAME:
			ErrorDialog( "Online_NameVerifyError",result );
			return TO_TITLE;
		case NETWORKBEGINRESULT_NO_PLUS:
			return TO_TITLE;
		default:
			ErrorDialog( "GameMode_OnlineFailed",result );
			return TO_TITLE;
		}
	}

	// オンラインモード用のサーバへ接続する
	while( true ) {
		result = signin.Connect();
		if( !result.IsSuccess() ) {
			if( DIALOG_YES == ErrorRetryDialog("GameMode_OnlineFailed",result) ) {
				return TO_TITLE;
			}
			continue;
		}
		break;
	}

	if ( IsEpic() )//接続出来たら所有権の確認
	{
		result = signin.CheckOwnerShip();
		if( !result.IsSuccess() )
		{
			Invitation_Clear();//念の為
			Dialog_Message( "EPIC_OWNERSHIP_FAILED" );
			return TO_TITLE;
		}
		
		WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ
		SearchUpdateAddon();	//追加コンテンツの更新開始
	}

	// オンラインミッションに入ったかをセーブして、一度でも入ったことがあればタイトルでログインをする
	if( IsSteam() ){
		pc_SaveReadyOnline(false, "Contents_AutoSaveRetry",true);	// セーブ開始
		WaitSaveLoad();
	}

	g_resource.Wait();
	// 待機ウインドウを消す
	wait.Close();

	// ミッション画像だけ先に読ませておく
	g_resource.EntryModeImage(0);

	wait.WaitClose();

	if( false == Network_IsCommunications() ) {
		UI chat = CreateChatRestrictUI();
		chat.WaitClose();
	}
	
	if ( IsEpic() )//所有権の再確認
	{
		WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ
		
		// SearchUpdateAddonを実行した時にModeNoが初期化されている為、オンラインモードに復旧
		SetMode(GetModeNo(GAME_ONLINE_SCENARIO,0));

		// モード、ゲームデータ読み込み
		if( LoadSaveData_ModeSelect() == false ){
			Dialog_Message( "Sys_LoadFailed_ToTitle" );

			return TO_TITLE;
		}
		
		UnlockDownloadContents();
		WaitSaveLoad();
	}
	

	// 招待されている場合は、参加先のルーム情報を読んできて参加する
	if( INVITATION_TYPE_NONE != GetInvitationType() ) {
		Invitation invite;
		int r;
		r = invite.Search();
		if( SUCCESS != r ) {
			Dialog_Message( "OnlineError_RoomError" );
			return TO_TITLE;
		}

		invite.Password();
		r = invite.Join();
		switch(r) {
		case SUCCESS:
			break;
		case NETWORKJOINRESULT_CHAT_RESTRICTION:
			Dialog_Message( "Lobby_Chat_NotInvite" );
			return TO_TITLE;
		case NETWORKJOINRESULT_UGC_RESTRICTION:
			Dialog_Message( "Lobby_UGC_NotInvite" );
			return TO_TITLE;
		case NETWORKJOINRESULT_FILLED:
			Dialog_Message( "OnlineError_RoomFull" );
			return TO_TITLE;
		default:
			Dialog_Message( "OnlineError_RoomError" );
			return TO_TITLE;
		}
		// 参加出来たのでルーム画面へ移行する
		Network_SetLocation(MENU_ROOM);
		return TO_ROOM;
	}

	return TO_LOBBY;
}

//===============================================================================
// サーバ選択画面
// オンラインモード
string OnlineMode()
{
	g_fade.Black();
	DeleteAllMenuUi();

	g_fade.In();

	g_music.Play( "BGM_E6M19_OnlineLobby" );	// BGM:メニュー画面

	g_resource.Entry("app:/ui/UiResourceGroup_Online.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.EntryModeImage(0);

	// この関数以降基本的に強制的にタイトルに戻される全体リセットが発生します。管理されていないメモリとかないようにしてください。
	OnlineInitializeResult next = _OnlineMode();

	g_fade.Black();

	switch( next ) {
	case TO_LOBBY:
		return "Lobby";
	case TO_ROOM:
		return "Room";
	case TO_CREATEROOM:
		return "CreateRoom";
	default:
		break;
	}

	g_music.Stop( 0 );
	return "StartToTitle";
}



//===============================================================================
// ルームから開始
string Debug_StartRoom()
{
	Invitation_Clear();

	g_music.Stop(g_music_fadetime);
	g_music.WaitStop();

	//初期化
	InitializeAll();
	Network_SetLocation(BOOT_COMPLETE);

	//タイトル
	titleSaveDataLoad(true);

	WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ
	WaitSaveLoad();

	SetMode(GetModeNo(GAME_ONLINE_SCENARIO,0));

	// モード、ゲームデータ読み込み
	if( LoadSaveData_ModeSelect() == false ){
		Dialog_Message( "Sys_LoadFailed_ToTitle" );

		return "StartToTitle";
	}
	UnlockDownloadContents();

	g_resource.Entry("app:/ui/UiResourceGroup_Online.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.EntryModeImage(0);

	if( _OnlineMode() == TO_LOBBY) {
		DebugRoomCreate creating;
		creating.CreateAndJoin();
		if( creating.Wait() ) {
			Network_SetLocation(MENU_ROOM);
			return "Room";
		}

		Dialog_Message( "Online_Game_Disconnect" );
	}

	return "StartToTitle";
}

//===============================================================================
// ロビーから開始
string Debug_StartLobby()
{
	Invitation_Clear();

	g_music.Stop(g_music_fadetime);
	g_music.WaitStop();

	//初期化
	InitializeAll();
	Network_SetLocation(BOOT_COMPLETE);

	//タイトル
	titleSaveDataLoad(true);

	WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ
	WaitSaveLoad();

	SetMode(GetModeNo(GAME_ONLINE_SCENARIO,0));

	// モード、ゲームデータ読み込み
	if( LoadSaveData_ModeSelect() == false ){
		Dialog_Message( "Sys_LoadFailed_ToTitle" );

		return "StartToTitle";
	}

	g_resource.Entry("app:/ui/UiResourceGroup_Online.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.EntryLoadinImage(0);

	UnlockDownloadContents();

	if( _OnlineMode() == TO_LOBBY) {
		g_resource.Wait();
		Network_SetLocation(MENU_LOBBY);
		return "Lobby";
	}

	return "StartToTitle";
}


//===============================================================================
// 本部画面から開始
string Debug_StartOffline()
{
	g_music.Stop(g_music_fadetime);
	g_music.WaitStop();

	//初期化
	InitializeAll();
	Network_SetLocation(BOOT_COMPLETE);

	//タイトル
	titleSaveDataLoad(true);

	WaitSearchUpdateAddon();	//追加コンテンツの更新終了を待つ
	WaitSaveLoad();

	SetMode(GetModeNo(GAME_OFFLINE_SCENARIO,0));

	// モード、ゲームデータ読み込み
	if( LoadSaveData_ModeSelect() == false ){
		Dialog_Message( "Sys_LoadFailed_ToTitle" );

		return "StartToTitle";
	}

	UnlockDownloadContents();

	return "HQMain";
}


bool ApplyModeNo(int mode_index)
{
	if (mode_index == GetCurrentModeNo()) {
		RestoreMissionSelect();
		// 既にロード済みなのでなにもしないようにする
	} else {
		g_resource.FreeGroup(RESOURCE_GROUP_MODE);

		ModeChangeFixup	gamemode;
		if (SetMode(mode_index)) {

			g_resource.SetSilent(true);
			g_resource.EntryModeImage(0);
			g_resource.SetSilent(false);

			// モード、ゲーム、実績データ読み込み
			if (LoadSaveData_ModeSelect()) {
				UpdateAchievementCounter(false, false);
				UnlockDownloadContents();

				gamemode.Restore();
			} else {
				gamemode.Release();
				// セーブデータのロードに失敗したのでタイトルに戻ります
				Dialog_Message("Sys_LoadFailed_ToTitle");
				return false;
			}
		} else {
			gamemode.Release();
			// コンテンツを所有していないのでタイトルに戻ります
			Dialog_Message("Lobby_NotHaveContents");

			return false;
		}
	}
	return true;
}

void _lobby_SetModeHandler(UI window, string message_id, string wparam)
{
	if ("SetModeRequest" == message_id) {
		// HUiLobbyからのコールバック、DLCモードとセーブデータのロードを行うために呼び出される

		// モード番号そのものがくるので、そのまま使用する
		int mode_no = parseInt(wparam);

		if (false == ApplyModeNo(mode_no)) {
			window.PostMessage("ModeRequestDone", "[result|false]");
		} else {
			window.PostMessage("ModeRequestDone", "[result|true]");
		}
	}
}

//===============================================================================
// ロビー画面
string Lobby()
{
	g_chat.Release();

	// ロビーに戻った段階で不用になっているネットワーク通知処理を掃除する（累積分の切断通知等）
	Network_ClearMessage();

	g_resource.Entry("app:/ui/UiResourceGroup_Online.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.Wait();

	g_bg.Play("app:/ui/lyt_bg.sgo");
	g_music.Play( "BGM_E6M19_OnlineLobby" );	// BGM:メニュー画面

	g_main_frame.Play("app:/ui/lyt_MainFrame.sgo");
	g_main_frame.GetObject().SetDrawOrder(g_fade.GetObject());

	// ロビー画面のＵＩ表示

	Network_SetLocation(MENU_LOBBY);

	string result = "";

	UI window = CreateUiFile("app:/ui/lyt_HUiOnlineLobby.sgo");
	window.SetDrawOrder(g_prev_object);
	g_fade.In();

	// 次の画面は同じリソースなのでプリロードを開始しておく
	g_resource.Entry("app:/ui/UiResourceGroup_OnlineRoom.sgo", SYSTEM_GROUP_SCENE, 0);

	string message_id;
	string wparam;
	while( window.GetMessage(message_id,wparam) ) {
		_lobby_SetModeHandler(window, message_id, wparam);
	}

	window.WaitCloseRequest();
	int exit_code = GetUiExitCode();

	switch( (exit_code&0xf) ){
	case NETWORKLOBBYMENU_CREATEROOM:
		result = "CreateRoom";
		break;

	case NETWORKLOBBYMENU_JOINROOM:
		result = "Room";
		break;

	case NETWORKLOBBYMENU_RETURN_TITLE:
		g_music.Stop( g_music_fadetime );
		g_fade.Out();
		g_resource.Wait();
		g_music.WaitStop();
		result = "StartToTitle";
		break;

	default:
		result = "exit";
		break;
	}

	// プレイヤーの選択で少なくとも以下に分岐する
	return result;
}

string CreateRoom()
{
	g_resource.Wait();

	g_bg.Play("app:/ui/lyt_bg.sgo");

	g_main_frame.Play("app:/ui/lyt_MainFrame.sgo");
	g_main_frame.GetObject().SetDrawOrder(g_fade.GetObject());

	g_music.Play( "BGM_E6M19_OnlineLobby" );

	UI main_object = CreateUiFile("app:/ui/lyt_HUiOnline_RoomCreate.sgo");
	g_prev_object = main_object;
	g_fade.In();

	string message_id;
	string wparam;
	while (main_object.GetMessage(message_id, wparam))
	{
		_lobby_SetModeHandler(main_object, message_id, wparam);
	}

	main_object.WaitCloseRequest();

	int exit_code = GetUiExitCode();

	string result = "Lobby";
	switch( exit_code ){
	case Hui_ROOMCREATE_MENU_CREATEROOM:
		Network_SetLocation(MENU_ROOM);
		//g_music.Stop( g_music_fadetime ); //ここでBGMをフェードするとRoomに入った途端に再生するのでおかしくなる
		result = "Room";
		break;

	case Hui_ROOMCREATE_MENU_RETURN_LOBBY:
		result = "Lobby";
		break;
	case Hui_ROOMCREATE_MENU_RETURN_TITLE:
		g_music.Stop( g_music_fadetime );
		g_fade.Out();
		g_resource.Wait();
		g_music.WaitStop();
		result = "StartToTitle";
		break;
	}

	return result;
}

string Room()
{
	g_resource.Entry("app:/ui/UiResourceGroup_OnlineRoom.sgo", SYSTEM_GROUP_SCENE, 0);
	g_resource.Wait();

	g_fade.Wait();

	g_chat.Build();
	Network_SetLocation(MENU_ROOM);

	g_bg.Play("app:/ui/lyt_bg.sgo");
	g_music.PlaySelectedMissionBGM_Start();   // 現在のミッションに設定されたBGMを再生する

	g_main_frame.Play("app:/ui/lyt_MainFrame.sgo");
	g_main_frame.GetObject().SetDrawOrder(g_fade.GetObject());

	UI ui_handle3D = CreateUiFile("app:/ui/lyt_HUiHQ3DModel.sgo");

	UI main_object = CreateUiFile("app:/ui/lyt_HUiOnlineRoom.sgo");
	g_prev_object = main_object;

	g_fade.In();

	string message_id;
	string wparam;
	while (main_object.GetMessage(message_id, wparam)) {
		_lobby_SetModeHandler(main_object, message_id, wparam);
	}

	main_object.WaitCloseRequest();
	int exit_code = GetUiExitCode();

	g_music.Stop( g_music_fadetime );

	print("ui_online_room exit code["+exit_code+"]");
	switch( exit_code ){
	case UIONLINE_GOTO_MISSION:
		g_fade.Out();
		g_fade.Wait();
		g_bg.Stop();

		ui_handle3D.Close();

		return "PlayMission_Online";
	case UIONLINE_GOTO_LOBBY:
		SaveAllData_ReturnTitle(false);
		break;
	case UIONLINE_GOTO_RETURNTITLE:
		ui_handle3D.Close();
		g_chat.Release();
		Network_LeaveRoom();

		g_music.Stop( g_music_fadetime );
		g_fade.Out();
		g_resource.Wait();
		g_music.WaitStop();
		return "StartToTitle";
	default:
		print("ハンドルされていないリザルトコードが返ってきています ["+exit_code+"]");
		break;
	}

	ui_handle3D.Close();

	// ロビーに戻す
	g_chat.Release();
	Network_LeaveRoom();

	// セーブ
	return "Lobby";
}

