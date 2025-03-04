// -*- coding: japanese-shift-jis -*-
//
// スクリプト共通部
//
// $HeadURL: https://svnrepos.sandlot.jp/svn/repos/FUSHIMI/trunk/Data/Mission/Common.h $
// $Id: Common.h 2 2018-04-09 10:43:07Z prg_t_noguchi $
//

const bool TRUE = true;
const bool FALSE = false;

// リダクションレベルを設定するためのダミー命令（スクリプトコンバート時に変換される）
void ps4_SetTextureReductionLevel(uint level) {}

void RegisterDefaultMob()
{
	RegisterMob("app:/object/man01.sgo", 1);
	RegisterMob("app:/object/man02.sgo", 1);
	RegisterMob("app:/object/man03.sgo", 1);
	RegisterMob("app:/object/woman01.sgo", 1);
	RegisterMob("app:/object/woman02.sgo", 1);
}

void RegisterDirtyMob()
{
	RegisterMob("app:/object/dirty_man01.sgo", 1);
	RegisterMob("app:/object/dirty_man02.sgo", 1);
	RegisterMob("app:/object/dirty_man03.sgo", 1);
	RegisterMob("app:/object/dirty_woman01.sgo", 1);
	RegisterMob("app:/object/dirty_woman02.sgo", 1);
}

void nw_Danti01_haikyo_ApplyMaterial()
{
	// ダートの強さを変更
	MapMaterial_SetValue_Float("", "dirt_adjust", 0.0);			 // 0-1
	MapMaterial_SetValue_Float("", "dirt_amount", 1.0);			 // 0-1
	MapMaterial_SetValue_Float("", "dirt_material_adjust", 1.0); // 0-1

	// 植え込みの草を茶色っぽく
	float r = 0.0;
	float g = 0.0;
	float b = 0.0;
	MapMaterial_MulValue_Float4("snd_Map_Simple_Clip", "diffuse", 0.52, 0.38, 0.24, 1);
	MapMaterial_MulValue_Float4("snd_Map_Build_Simple_Clip", "diffuse", 0.58, 0.55, 0.44, 1);
	MapMaterial_MulValue_Float4("snd_BRDF_Map_Common_Clip", "diffuse", 0.52, 0.38, 0.24, 1);

	// 小物のマテリアル変更
	array<string> target_list = {"snd_Map_Object", "snd_Map_Object_NoAO", "snd_Map_Object_NoAO_Light", "snd_Map_Object_NoAO_Dirt", "snd_Map_Object_NoCC", "snd_Map_Object_NoCCAO"};
	for (uint i = 0; i < target_list.length(); i++)
	{
		MapMaterial_MulValue_Float4(target_list[i], "diffuse", 0.58, 0.55, 0.44, 1); // 茶色っぽく
		MapMaterial_ClampValue_Float(target_list[i], "roughness", 0.5, 1);			 // roughness の範囲を制限して表面を荒くする
	}

	// 発光を消す
	MapMaterial_SetValue_Float4("", "light_color", 0, 0, 0, 1);
	MapMaterial_SetValue_Float("snd_Map_Object_NoAO_Light", "roughness", 1); // 表面を荒くする
}

// #define TEAM_ID_PLAYER 0
// #define TEAM_ID_ENEMY 1
// #define TEAM_ID_FRIEND 2
// #define TEAM_ID_NEUTRAL 3
// #define TEAM_ID_VEHICLE 5

// enum DialogFlags
// {
// 	DIALOG_FLAG_DEFAULT_NO = 1 << 0,
// 	DIALOG_FLAG_CANCEL_BUTTON = 1 << 1,
// };

// enum DialogResult
// {
// 	DIALOG_RESULT_UNKNOWN,
// 	DIALOG_RESULT_OK_YES,
// 	DIALOG_RESULT_NO,
// 	DIALOG_RESULT_CANCEL,
// };

//===============================================================================
// ミッション失敗イベント
void MissionGameOverEvent()
{
	// ミッション終了処理を開始する（他のイベントを起動させない状態）
	if (internal_BeginFinishing() == false)
	{
		// すでに終了処理が開始済みの場合は帰る
		return;
	}

	Online_GameOver();
	Wait(3.0f);

	internal_SetEnablePause(false); // 以降ポーズ禁止。

	StopBgm(2.0f);
	Wait(1.5f);

	if (IsOnlineMode())
	{
		// 切断されていたら待機
		Online_DisconnectedWait();
	}

	// ミッション失敗表示
	UI failed_bg = CreateUI_File("app:/ui/lyt_HUiMissionFailed.sgo");

	// Bgm("Jingle_MissionFailed");
	Bgm("Jingle_E6_MissionFailed");

	Wait(5.0f);
	Online_GameOverWait();

	if (IsOnlineMode())
	{
		// 切断されていたら待機
		Online_DisconnectedWait();
	}

	if (sys_IsDemoMode() == false)
	{
		UI failed_result_ui = CreateUI_File("app:/ui/lyt_HUiFailedResult.sgo");
		failed_result_ui.WaitClose();
	}

	//	result = Dialog_YesNo( "GameOver_Retry", "", 0 );
	Dialog dialog;
	dialog.OpenMissionFailed();
	dialog.WaitClose();
	Dialog_MissionFailedResult result = dialog.GetMissionFailedResult();
	// Dialog_MissionFailedResult result = dialog.MissionFailed();

	UI fade = CreateUI("ui_fade_screen_simple");
	fade.Fade_Control(FADE_CONTROL_IN_TO_OUT, 0.5f);
	fade.Fade_WaitComplete();
	if (result == MISSIONFAILED_DIALOG_RESULT_RESTART)
	{
		print("retry");
		internal_Exit(MISSION_RESULT_RETRY);
	}
	else
	{
		print("abort");
		internal_Exit(MISSION_RESULT_ABORT);
	}
}

//===============================================================================
// 音声系補助

void Voice2(string cue_name, float wait_time)
{
	Voice(cue_name);
	WaitVoice();
	Wait(wait_time);
}

void RadioBegin()
{
	internal_Voice("MusenBegin", false);
}
void RadioEnd()
{
	internal_Voice("MusenEnd", false);
}

void RadioVoice(string cue_name, float wait_time)
{
	WaitVoice();
	Wait(wait_time);
	RadioBegin();
	Voice(cue_name);
	RadioEnd();
	WaitVoice();
}

void DebugMessageW(string message, float second)
{
	ClearDebugMessage();
	DebugMessage(message, second);
	Wait(second + 0.1);
}

// ミッション組用の仮メッセージ表示
void TempMessage(string message, float second)
{
	ClearDebugMessage();
	DebugMessage("[仮] " + message, second);
}
void TempMessageW(string message, float second)
{
	TempMessage(message, second);
	Wait(second);
}

// 一人に喋らせる
void Speak_Single(Object object, string voice, uint32 flags, float wait)
{
	WaitVoice();
	TalkBegin();
	Talk_AddSingleAuto(object, voice, "", flags, 0);
	TalkEnd();
	WaitVoice();
	Wait(wait);
}

// 複数キャラクタに喋らせる
void Speak_Multi(ObjectGroup group, uint32 count, string voice, string motion, float delay, float wait)
{
	WaitVoice();
	TalkBegin();
	Talk_AddMulti(group, count, voice, motion, 0, delay, 0xffffffff);
	TalkEnd();
	WaitVoice();
	Wait(wait);
}

// 新仕様のラジオ音声
void Speak_Radio(string voice, float wait)
{
	WaitVoice();
	TalkBegin();
	Talk_AddRadio(voice + "_E");
	TalkEnd();
	// RadioBegin();
	// Voice(voice + "_E");
	// RadioEnd();
	WaitVoice();
	Wait(wait);
}

//===============================================================================
//
// 味方オブジェクトの作成
//

// 軍曹達を作成する
Object g_sergent;
Object g_sergent_follower1;
Object g_sergent_follower2;
Object g_sergent_follower3;

Object CreateSergent(string point, float level, bool is_auto_follow)
{
	g_sergent = CreateFriend(point, "app:/object/AiArmySoldier_S_AF_Leader.sgo", level, is_auto_follow).SetAutoResurrection(true);
	return g_sergent;
}

void CreateSergentFollower(string point, float radius, float level, bool is_auto_follow)
{
	g_sergent_follower1 = CreateFriend(point, "app:/object/AiArmySoldier_S_Follower1.sgo", level, is_auto_follow).SetAutoResurrection(true);
	g_sergent_follower2 = CreateFriend(point, "app:/object/AiArmySoldier_S_Follower2.sgo", level, is_auto_follow).SetAutoResurrection(true);
	g_sergent_follower3 = CreateFriend(point, "app:/object/AiArmySoldier_S_Follower3.sgo", level, is_auto_follow).SetAutoResurrection(true);
}

void CreateSergentFollower2(string point1, string point2, string point3, float level, bool is_auto_follow)
{
	g_sergent_follower1 = CreateFriend(point1, "app:/object/AiArmySoldier_S_Follower1.sgo", level, is_auto_follow).SetAutoResurrection(true);
	g_sergent_follower2 = CreateFriend(point2, "app:/object/AiArmySoldier_S_Follower2.sgo", level, is_auto_follow).SetAutoResurrection(true);
	g_sergent_follower3 = CreateFriend(point3, "app:/object/AiArmySoldier_S_Follower3.sgo", level, is_auto_follow).SetAutoResurrection(true);
}

Object CreateSergentSquad(string point, float radius, float level, bool is_auto_follow)
{
	CreateSergent(point, level, is_auto_follow);
	ObjectGroup group = CreateFriendGroup(point, radius, "app:/object/AiArmySoldier_S_Follower1.sgo;app:/object/AiArmySoldier_S_Follower2.sgo;app:/object/AiArmySoldier_S_Follower3.sgo", 3, level, true)
							.SetAiFollow(g_sergent)
							.SetAutoResurrection(true);
	g_sergent_follower1 = group[0];
	g_sergent_follower2 = group[1];
	g_sergent_follower3 = group[2];
	return g_sergent;
}

Object CreateSergent_n605(string point, float level, bool is_auto_follow)
{
	g_sergent = CreateFriend(point, "app:/object/n605_Sergent_Blazer.sgo", level, is_auto_follow).SetAutoResurrection(true);
	return g_sergent;
}

Object CreateSergentSquad_n605(string point, float radius, float level, bool is_auto_follow)
{
	CreateSergent_n605(point, level, is_auto_follow);
	ObjectGroup group = CreateFriendGroup(point, radius, "app:/object/n605_SergentFollower1.sgo;app:/object/n605_SergentFollower2.sgo;app:/object/n605_SergentFollower3.sgo", 3, level, true)
							.SetAiFollow(g_sergent)
							.SetAutoResurrection(true);
	g_sergent_follower1 = group[0];
	g_sergent_follower2 = group[1];
	g_sergent_follower3 = group[2];
	return g_sergent;
}

Object CreateSergentSquad_OMG(string point, float radius, float level, bool is_auto_follow)
{
	g_sergent = CreateFriend(point, "app:/object/AiArmySoldier_S_OMG_Leader.sgo", level, is_auto_follow).SetAutoResurrection(true);
	ObjectGroup group = CreateFriendGroup(point, radius, "app:/object/AiArmySoldier_S_Follower1.sgo;app:/object/AiArmySoldier_S_Follower2.sgo;app:/object/AiArmySoldier_S_Follower3.sgo", 3, level, true)
							.SetAiFollow(g_sergent)
							.SetAutoResurrection(true);
	g_sergent_follower1 = group[0];
	g_sergent_follower2 = group[1];
	g_sergent_follower3 = group[2];
	return g_sergent;
}

void CreateSergentFollower2_n605(string point1, string point2, string point3, float level, bool is_auto_follow)
{
	g_sergent_follower1 = CreateFriend(point1, "app:/object/n605_SergentFollower1.sgo", level, is_auto_follow).SetAutoResurrection(true);
	g_sergent_follower2 = CreateFriend(point2, "app:/object/n605_SergentFollower2.sgo", level, is_auto_follow).SetAutoResurrection(true);
	g_sergent_follower3 = CreateFriend(point3, "app:/object/n605_SergentFollower3.sgo", level, is_auto_follow).SetAutoResurrection(true);
}

//
// グリムリーパー￥
//
Object g_grimreaper;
Object g_spriggan;

//
// 大佐
//
Object g_colonel;
Object g_colonel_follower1;
Object g_colonel_follower2;
Object g_colonel_follower3;
Object g_colonel_follower4;

Object CreateColonel(string point, float level, bool is_auto_follow)
{
	g_colonel = CreateFriend(point, "app:/object/n603_colonel_AF.sgo", level, is_auto_follow).SetAutoResurrection(true);
	return g_colonel;
}

Object CreateColonel_NoWeapon(string point, float level, bool is_auto_follow)
{
	g_colonel = CreateFriend(point, "app:/object/n603_colonel_noweapon.sgo", level, is_auto_follow).SetAutoResurrection(true);
	return g_colonel;
}

Object CreateColonelSquad(string point, float radius, string slave_path, int slave_count, float level, bool is_auto_follow)
{
	g_colonel = CreateFriendSquad(point, radius, "app:/object/n603_colonel_AF.sgo", slave_path, slave_count, level, is_auto_follow);
	g_colonel.SetAutoResurrection(true);
	for (int i = 0; i != slave_count; i++)
	{
		Object f = g_colonel.GetFollowerObject(i);
		f.SetAutoResurrection(true);
		if (i < 4)
		{
			f.internal_SetUniqueTalk().SetTalkVariationID(i);
		}
	}
	g_colonel_follower1 = g_colonel.Follower(0);
	g_colonel_follower2 = g_colonel.Follower(1);
	g_colonel_follower3 = g_colonel.Follower(2);
	g_colonel_follower4 = g_colonel.Follower(3);

	return g_colonel;
}

Object g_lieutenant;
Object g_lieutenant_follower1;
Object g_lieutenant_follower2;
Object g_lieutenant_follower3;
Object g_lieutenant_follower4;

// オブジェクトを中尉に設定
void internal_SetLieutenant(Object o)
{
//	o.internal_SetUniqueTalk();
//	o.SetTalkVariationID(0);
//	o.SetTalkTable("app:/sound/lieutenant_talk.sgo");
	o.SetAutoResurrection(true);
}

Object CreateLieutenant(string point, string lieutenant_path, float level, bool is_auto_follow)
{
	g_lieutenant = CreateFriend(point, lieutenant_path, level, is_auto_follow);
	internal_SetLieutenant(g_lieutenant);
	return g_lieutenant;
}

// 中尉の小隊を作成
Object CreateLieutenantSquad(string point, float radius, string lieutenant_path, string slave_path, int slave_count, float level, bool is_auto_follow)
{
	g_lieutenant = CreateFriendSquad(point, radius, lieutenant_path, slave_path, slave_count, level, is_auto_follow);
	g_lieutenant.SetAutoResurrection(true);
	internal_SetLieutenant(g_lieutenant);
	for (int i = 0; i != slave_count; i++)
	{
		Object f = g_lieutenant.GetFollowerObject(i);
		f.SetAutoResurrection(true);
		if (i < 4)
		{
//			f.internal_SetUniqueTalk().SetTalkVariationID(i);
		}
	}
	g_lieutenant_follower1 = g_lieutenant.Follower(0);
	g_lieutenant_follower2 = g_lieutenant.Follower(1);
	g_lieutenant_follower3 = g_lieutenant.Follower(2);
	g_lieutenant_follower4 = g_lieutenant.Follower(3);
	return g_lieutenant;
}

//
// プロフェッサー
//
Object g_professor;

Object CreateProfessor(string point, float level, bool is_auto_follow)
{
	g_professor = CreateFriend(point, "app:/object/n602_professor_AF.sgo", level, is_auto_follow).SetAutoResurrection(true);
	return g_professor;
}

Object CreateProfessor_NoWeapon(string point, float level, bool is_auto_follow)
{
	g_professor = CreateFriend(point, "app:/object/n602_professor_noweapon.sgo", level, is_auto_follow).SetAutoResurrection(true);
	return g_professor;
}

Object CreateProfessor_Brazer(string point, float level, bool is_auto_follow)
{
	g_professor = CreateFriend(point, "app:/object/n602_professor_brazer.sgo", level, is_auto_follow).SetAutoResurrection(true);
	return g_professor;
}
Object CreateProfessorSquad(string point, float radius, string slave_path, int slave_count, float level, bool is_auto_follow)
{
	g_professor = CreateFriendSquad(point, radius, "app:/object/n602_professor_AF.sgo", slave_path, slave_count, level, is_auto_follow);
	g_professor.SetAutoResurrection(true);
	return g_professor;
}

//
// 伍長
//
Object g_corporal;
Object CreateCorporal(string point, float level, bool is_auto_follow)
{
	g_corporal = CreateFriend(point, "app:/object/n601_corporal_AF.sgo", level, is_auto_follow).SetAutoResurrection(true);
	return g_corporal;
}

Object CreateCorporal_n604(string point, float level, bool is_auto_follow)
{
	g_corporal = CreateFriend(point, "app:/object/n604_corporal_AF.sgo", level, is_auto_follow).SetAutoResurrection(true);
	return g_corporal;
}

Object CreateCorporal_n604_Squad(string point, float radius, string slave_path, int slave_count, float level, bool is_auto_follow)
{
	g_corporal = CreateFriendSquad(point, radius, "app:/object/n604_corporal_AF.sgo", slave_path, slave_count, level, is_auto_follow);
	g_corporal.SetAutoResurrection(true);
	return g_corporal;
}

//===============================================================================
// ミッションクリア共通処理
void MissionClear_Common(float wait_sec, string ui_path)
{
	// if (IsOnlineMode())
	// {
	// 	// 切断されていたら待機
	// 	Online_DisconnectedWait();
	// }

	// ミッションクリア表示
	UI clear_bg_handle = CreateUI_File(ui_path);

	Wait(wait_sec);

	UI fade = CreateUI("ui_fade_screen_simple");
	fade.Fade_Control(FADE_CONTROL_IN_TO_OUT, 3.0f);
	fade.Fade_WaitComplete();

	// Exit に設定した結果を MissionMgr::GetScriptResult から取得して MainScript を分岐させる
	internal_Exit(MISSION_RESULT_CLEAR);
}

// ミッションクリア共通処理 ( フェード時間指定付き )
void MissionClear_Common2(float wait_sec, string ui_path, float fade_sec = 3)
{
	// if (IsOnlineMode())
	// {
	// 	// 切断されていたら待機
	// 	Online_DisconnectedWait();
	// }

	// ミッションクリア表示
	UI clear_bg_handle = CreateUI_File(ui_path);

	Wait(wait_sec);

	UI fade = CreateUI("ui_fade_screen_simple");
	fade.Fade_Control(FADE_CONTROL_IN_TO_OUT, fade_sec);
	fade.Fade_WaitComplete();

	// Exit に設定した結果を MissionMgr::GetScriptResult から取得して MainScript を分岐させる
	internal_Exit(MISSION_RESULT_CLEAR);
}

//
// ミッションクリア時
//
void MissionClear_EDF5()
{
	// 	$ "mission clear";

	StopBgm(2.0f);
	Wait(1.5f);

	internal_SetEnablePause(false); // ポーズ類を閉じて以降ポーズ禁止。

	Bgm("Jingle_MissionCleared");

	MissionClear_Common(6.0f, "app:/ui/lyt_HUiMissionCleared.sgo");
}

//
// 最終ミッションクリア時
//
void FinalMissionClear_EDF5()
{
	StopBgm(2.0f);
	Wait(1.5f);

	internal_SetEnablePause(false); // ポーズ類を閉じて以降ポーズ禁止。

	Bgm("Jingle_MissionClearedFinal");

	MissionClear_Common(10.0f, "app:/ui/lyt_HUiMissionComplete.sgo");
}

//
// ミッション撤退クリア時
//
void MissionEscapeClear_EDF5()
{
	StopBgm(2.0f);
	Wait(1.5f);

	internal_SetEnablePause(false); // ポーズ類を閉じて以降ポーズ禁止。

	Bgm("Jingle_MissionEscape");

	MissionClear_Common(7.0f, "app:/ui/lyt_HUiMissionCleared.sgo");
}

//
// ミッションクリア時（EDF6）
//
void MissionClear()
{
	// 	$ "mission clear";

	StopBgm(2.0f);
	Wait(1.5f);

	internal_SetEnablePause(false); // ポーズ類を閉じて以降ポーズ禁止。

	// Bgm("Jingle_MissionCleared");
	Bgm("Jingle_E6_MissionCleared");

	MissionClear_Common(6.0f, "app:/ui/lyt_HUiMissionCleared.sgo");
}

//
// 最終ミッションクリア時（EDF6）
//
void FinalMissionClear()
{
	StopBgm(2.0f);
	Wait(1.5f);

	internal_SetEnablePause(false); // ポーズ類を閉じて以降ポーズ禁止。

	// Bgm("Jingle_MissionClearedFinal");
	Bgm("Jingle_E6_MissionClearedFinal");

	MissionClear_Common(10.0f, "app:/ui/lyt_HUiMissionComplete.sgo");
}

//
// ミッション撤退クリア時（EDF6）
//
void MissionEscapeClear()
{
	StopBgm(2.0f);
	Wait(1.5f);

	internal_SetEnablePause(false); // ポーズ類を閉じて以降ポーズ禁止。

	// Bgm("Jingle_MissionEscape");
	Bgm("Jingle_E6_MissionEscape");

	MissionClear_Common(7.0f, "app:/ui/lyt_HUiMissionCleared.sgo");
}

//
// ミッションクリア（EDF6 歴史改変時）
//
void MissionClear_Kaihen()
{
	// 	$ "mission clear";

	StopBgm(2.0f);
	Wait(1.5f);

	internal_SetEnablePause(false); // ポーズ類を閉じて以降ポーズ禁止。

	// Bgm("Jingle_MissionCleared");
	Bgm("Jingle_E6_MissionClearedTimeMachine");

	MissionClear_Common(6.0f, "app:/ui/lyt_HUiMissionCleared.sgo");
}

//
// ミッションクリア（EDF6 タイムマシン暴走）
//
void MissionClear_TimeMachine()
{
	// 	$ "mission clear";

	StopBgm(2.0f);
	Wait(1.5f);

	internal_SetEnablePause(false); // ポーズ類を閉じて以降ポーズ禁止。

	// Bgm("Jingle_MissionCleared");
	Bgm("Jingle_E6_MissionClearedKaihen");

	MissionClear_Common(6.0f, "app:/ui/lyt_HUiMissionCleared.sgo");
}

//
// ミッションクリア時（EDF6 MissionPack2）
//
void MissionClear_MissionPack2()
{
	// 	$ "mission clear";

	StopBgm(2.0f);
	Wait(1.5f);

	internal_SetEnablePause(false); // ポーズ類を閉じて以降ポーズ禁止。

	// Bgm("Jingle_MissionCleared");
	Bgm("Jingle_E6_MissionCleared");

	MissionClear_Common2(8.0f, "app:/ui/lyt_HUiMissionCleared.sgo", 8.0f);
}

//===============================================================================
//
// 深海怪獣用フォグシーンに設定
bool g_is_fog_begin = false;

void Merman_FogScene(float second, float near, float far, float apply_ratio)
{
	EventLightTool tool;

	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_BG_APPLY, apply_ratio, 0, 0, 0, second);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_COLOR, 0.5, 0.5, 0.5, apply_ratio, second);
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_FOG_DISTANCE,
		near,
		far, // 値を大きくすると霧が遠くに表示されるので遠くまで見えるようになり、小さくすると近くしか見えなくなる
		0, 0, second);
	if (g_is_fog_begin == false)
	{
		g_is_fog_begin = true;
		SceneEffect_Fog(
			0.0,  // フェード値
			0.01, // パーティクルが流れる速さ
			1,	  // パーティクルが流れる方向ベクトル(X)
			0.5	  // パーティクルが流れる方向ベクトル(Z)
		);
		SceneEffect_StartFade(0.125 * apply_ratio /*目標フェード値(0～1)*/, second /*フェード時間*/);
	}
}

void Merman_FogScene(float second, float near, float far)
{
	Merman_FogScene(second, near, far, 1);
}

void Merman_FogScene(float second)
{
	Merman_FogScene(second, 200, 1000);
}

void Merman_FogRevert(float second, float ratio)
{
	EventLightTool tool;
	tool.RevertEnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_BG_APPLY, ratio, second);
	tool.RevertEnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_COLOR, ratio, second);
	tool.RevertEnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_DISTANCE, ratio, second);

	SceneEffect_StartFade(0.25 * (1 - ratio) /*目標フェード値(0～1)*/, second /*フェード時間*/);
}

//
// 歴史改変時の天候設定
//
void SetAlternateHistorySky(float fade_second)
{
	EventLightTool tool;

	// ライト色を変更
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_LIGHT0_COLOR, // アニメーションさせるパラメータタイプ
		0.765,							   // x
		0.429,							   // y
		0.721,							   // z
		1,								   // w
		fade_second						   // アニメーション時間
	);
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_LIGHT1_COLOR, // アニメーションさせるパラメータタイプ
		0.541,							   // x
		0.136,							   // y
		0.441,							   // z
		1,								   // w
		fade_second						   // アニメーション時間
	);
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_LIGHT2_COLOR, // アニメーションさせるパラメータタイプ
		0.313,							   // x
		0.431,							   // y
		0.338,							   // z
		1,								   // w
		fade_second						   // アニメーション時間
	);
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_LIGHT3_COLOR, // アニメーションさせるパラメータタイプ
		0.051,							   // x
		0.200,							   // y
		0.072,							   // z
		1,								   // w
		fade_second						   // アニメーション時間
	);
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_AMBIENT_COLOR, // アニメーションさせるパラメータタイプ
		0.098,								// x
		0.173,								// y
		0.102,								// z
		1,									// w
		fade_second							// アニメーション時間
	);

	// スペキュラ光
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_LIGHT0_SPECULAR_COLOR,
		0.135,		// x(r)
		0.028,		// y(g)
		0.141,		// z(b)
		1,			// w(a)
		fade_second // アニメーション時間
	);

	// サブスペキュラ光1
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_LIGHT1_SPECULAR_COLOR,
		0.247,		// x(r)
		0.088,		// y(g)
		0.226,		// z(b)
		1,			// w(a)
		fade_second // アニメーション時間
	);

	// サブスペキュラ光2
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_LIGHT2_SPECULAR_COLOR,
		0.065,		// x(r)
		0.102,		// y(g)
		0.100,		// z(b)
		1,			// w(a)
		fade_second // アニメーション時間
	);

	// サブスペキュラ光3
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_LIGHT3_SPECULAR_COLOR,
		0.072,		// x(r)
		0.106,		// y(g)
		0.089,		// z(b)
		1,			// w(a)
		fade_second // アニメーション時間
	);

	// // フォグだけいじると背景となじまないので、背景にもフォグをかけてみる
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_FOG_BG_APPLY, // アニメーションさせるパラメータタイプ
	// 	1,								   // x
	// 	0,								   // y
	// 	0,								   // z
	// 	0,								   // w
	// 	fade_second						   // アニメーション時間
	// );

	// Wait(5 /*この命令で停止する秒数*/);

	// // フォグ色を変更
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_FOG_COLOR, // アニメーションさせるパラメータタイプ
	// 	1,								// x
	// 	0,								// y
	// 	0,								// z
	// 	1,								// w
	// 	fade_second						// アニメーション時間
	// );

	// 太陽の色
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_SUN_COLOR, // アニメーションさせるパラメータタイプ
		0.25,							// x
		1.4,							// y
		0.14,							// z
		1,								// w
		fade_second						// アニメーション時間
	);
	// 太陽周辺の色
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_SUN_HALO_COLOR, // アニメーションさせるパラメータタイプ
		0.2 * 0.5,							 // x
		1.0 * 0.5,							 // y
		0.013 * 0.5,						 // z
		0.5,								 // w
		fade_second							 // アニメーション時間
	);
	// 空の色
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_SKY_COLOR, // アニメーションさせるパラメータタイプ
		0.380,							// x
		0.107,							// y
		0.172,							// z
		1,								// w
		fade_second						// アニメーション時間
	);
	// フォグ色を変更
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_FOG_COLOR, // アニメーションさせるパラメータタイプ
		0.122,							// x
		0.038,							// y
		0.081,							// z
		0.9,							// w
		fade_second						// アニメーション時間
	);
	// フォグ色を変更
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_BRIGHTNESS_FOG_COLOR, // アニメーションさせるパラメータタイプ
		0.173,									   // x
		0.051,									   // y
		0.111,									   // z
		0.894,									   // w
		fade_second								   // アニメーション時間
	);
}

//
// 歴史改変時の天候設定
//
void SetAlternateHistorySky2(float fade_second)
{
	EventLightTool tool;

	// ライト色を変更
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_LIGHT0_COLOR, // アニメーションさせるパラメータタイプ
		0.72,							   // x
		0.58,							   // y
		0.7,							   // z
		1,								   // w
		fade_second						   // アニメーション時間
	);
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_LIGHT1_COLOR, // アニメーションさせるパラメータタイプ
	// 	0.541,							   // x
	// 	0.136,							   // y
	// 	0.441,							   // z
	// 	1,								   // w
	// 	fade_second						   // アニメーション時間
	// );
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_LIGHT2_COLOR, // アニメーションさせるパラメータタイプ
	// 	0.313,							   // x
	// 	0.431,							   // y
	// 	0.338,							   // z
	// 	1,								   // w
	// 	fade_second						   // アニメーション時間
	// );
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_LIGHT3_COLOR, // アニメーションさせるパラメータタイプ
	// 	0.051,							   // x
	// 	0.200,							   // y
	// 	0.072,							   // z
	// 	1,								   // w
	// 	fade_second						   // アニメーション時間
	// );
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_AMBIENT_COLOR, // アニメーションさせるパラメータタイプ
	// 	0.098,								// x
	// 	0.173,								// y
	// 	0.102,								// z
	// 	1,									// w
	// 	fade_second							// アニメーション時間
	// );

	// //スペキュラ光
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_LIGHT0_SPECULAR_COLOR,
	// 	0.135,		// x(r)
	// 	0.028,		// y(g)
	// 	0.141,		// z(b)
	// 	1,			// w(a)
	// 	fade_second // アニメーション時間
	// );

	// //サブスペキュラ光1
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_LIGHT1_SPECULAR_COLOR,
	// 	0.247,		// x(r)
	// 	0.088,		// y(g)
	// 	0.226,		// z(b)
	// 	1,			// w(a)
	// 	fade_second // アニメーション時間
	// );

	// //サブスペキュラ光2
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_LIGHT2_SPECULAR_COLOR,
	// 	0.065,		// x(r)
	// 	0.102,		// y(g)
	// 	0.100,		// z(b)
	// 	1,			// w(a)
	// 	fade_second // アニメーション時間
	// );

	// //サブスペキュラ光3
	// tool.EnvFadeAnimation(
	// 	EVENT_LIGHT_ENV_FADE_LIGHT3_SPECULAR_COLOR,
	// 	0.072,		// x(r)
	// 	0.106,		// y(g)
	// 	0.089,		// z(b)
	// 	1,			// w(a)
	// 	fade_second // アニメーション時間
	// );

	// 太陽の色
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_SUN_COLOR, // アニメーションさせるパラメータタイプ
		0.25,							// x
		1.4,							// y
		0.14,							// z
		1,								// w
		fade_second						// アニメーション時間
	);
	// 太陽周辺の色
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_SUN_HALO_COLOR, // アニメーションさせるパラメータタイプ
		0.2 * 0.5,							 // x
		1.0 * 0.5,							 // y
		0.013 * 0.5,						 // z
		0.5,								 // w
		fade_second							 // アニメーション時間
	);
	// 空の色
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_SKY_COLOR, // アニメーションさせるパラメータタイプ
		0.380,							// x
		0.107,							// y
		0.172,							// z
		1,								// w
		fade_second						// アニメーション時間
	);
	// フォグ色を変更
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_FOG_COLOR, // アニメーションさせるパラメータタイプ
		0.122,							// x
		0.038,							// y
		0.081,							// z
		0.9,							// w
		fade_second						// アニメーション時間
	);
	// フォグ色を変更
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_BRIGHTNESS_FOG_COLOR, // アニメーションさせるパラメータタイプ
		0.173,									   // x
		0.051,									   // y
		0.111,									   // z
		0.894,									   // w
		fade_second								   // アニメーション時間
	);
}

//
// 闇夜の環境に設定
//
void SetDarkEnv(float fog_near, float fog_far, float sky_r, float sky_g, float sky_b)
{
	EventLightTool tool;
	tool.EnvMode(EVENT_LIGHT_ENV_UNDERGROUND);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_LIGHT0_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_LIGHT0_SPECULAR_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_LIGHT1_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_LIGHT1_SPECULAR_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_LIGHT2_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_LIGHT2_SPECULAR_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_LIGHT3_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_LIGHT3_SPECULAR_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_AMBIENT_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_COLOR, 0, 0, 0, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_DISTANCE, fog_near, fog_far, 0, 0, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_SKY_COLOR, sky_r, sky_g, sky_b, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_SUN_COLOR, sky_r, sky_g, sky_b, 1, 0);
	tool.EnvFadeAnimation(EVENT_LIGHT_ENV_FADE_SUN_HALO_COLOR, sky_r, sky_g, sky_b, 1, 0);
	// tool.RevertAllEnvFadeAnimation(0.1, 0); //  全てのライト設定を少し戻す
}

#if IGNORE

//===============================================================================
// 環境エフェクト 雪
void SceneEffect_Snow(
	float fade,				   // フェード値。雪を積もらせるハイトマップの高さ
	float clip_angle,		   // 最大限に雪を積もらせる法線の向き
	int particle_count,		   // パーティクルの個数
	float particle_fall_speed) // パーティクルの落下速度
{
	internal_SceneEffect_Snow(
		10,
		0.1f,
		0.05f,
		clip_angle,
		fade,
		0.5f, 0.5f, 0.5f,
		2, 2, 2,
		100,
		particle_count,
		40.f,
		particle_fall_speed);
}

//===============================================================================
// 環境エフェクト 雨
void SceneEffect_Rain(
	float fade,				   // フェード値
	float reflection,		   // 濡れている部分の反射の強さ
	float uv_animation_speed,  // 濡れている部分のUVアニメーションのスピード
	int particle_count,		   // パーティクルの個数
	float particle_fall_speed, // パーティクルの落下速度
	float particle_alpha)	   // パーティクルの不透明度
{
	internal_SceneEffect_Rain(
		fade,
		reflection,
		0.5f,
		uv_animation_speed,
		1.f,
		2.0f, 2.0f, 2.0f,
		200.f,
		particle_count,
		40.f,
		particle_fall_speed,
		particle_alpha);
}

//===============================================================================
// 環境エフェクト 雨
void SceneEffect_RainEx(
	float fade,				   // フェード値
	float reflection,		   // 濡れている部分の反射の強さ
	float uv_animation_speed,  // 濡れている部分のUVアニメーションのスピード
	float wet_normal_power,	   // 濡れている部分の強調具合
	int particle_count,		   // パーティクルの個数
	float particle_fall_speed, // パーティクルの落下速度
	float particle_alpha)	   // パーティクルの不透明度
{
	internal_SceneEffect_Rain(
		fade,
		reflection,
		0.5f,
		uv_animation_speed,
		wet_normal_power,
		2.0f, 2.0f, 2.0f,
		200.f,
		particle_count,
		40.f,
		particle_fall_speed,
		particle_alpha);
}

//===============================================================================
// 環境エフェクト 砂埃
void SceneEffect_FugitiveDust(
	float fade,					// フェード値
	int particle_count,			// パーティクルの個数
	float particle_speed,		// パーティクルが流れる速さ
	float particle_direction_x, // パーティクルが流れる方向ベクトル(X)
	float particle_direction_y, // パーティクルが流れる方向ベクトル(Y)
	float particle_direction_z) // パーティクルが流れる方向ベクトル(Z)
{
	internal_SceneEffect_FugitiveDust(
		fade,
		particle_count,
		10.f,
		particle_speed,
		particle_direction_x,
		particle_direction_y,
		particle_direction_z);
}

//===============================================================================
// 環境エフェクト 霧
void SceneEffect_Fog(
	float fade,					// フェード値
	int particle_count,			// パーティクルの個数
	float particle_speed,		// パーティクルが流れる速さ
	float particle_direction_x, // パーティクルが流れる方向ベクトル(X)
	float particle_direction_y, // パーティクルが流れる方向ベクトル(Y)
	float particle_direction_z) // パーティクルが流れる方向ベクトル(Z)
{
	internal_SceneEffect_Fog(
		fade,
		particle_count,
		10.f,
		particle_speed,
		particle_direction_x,
		particle_direction_y,
		particle_direction_z);
}

#endif

//
// 真っ白からフェードインする
//
void WhiteIn(float second)
{
	EventLightTool tool;
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_FOG_COLOR, // アニメーションさせるパラメータタイプ
		4,								// x(r)
		4,								// y(g)
		4,								// z(b)
		1,								// w(a)
		0								// アニメーション時間
	);
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_FOG_BG_APPLY, // アニメーションさせるパラメータタイプ
		1,								   // x(r)
		1,								   // y(g)
		1,								   // z(b)
		1,								   // w(a)
		0								   // アニメーション時間
	);
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_FOG_DISTANCE, // アニメーションさせるパラメータタイプ
		-10000,							   // x(r)
		0,								   // y(g)
		0,								   // z(b)
		1,								   // w(a)
		0								   // アニメーション時間
	);

	// 空の色
	tool.EnvFadeAnimation(
		EVENT_LIGHT_ENV_FADE_SKY_COLOR, // アニメーションさせるパラメータタイプ
		8,								// x
		8,								// y
		8,								// z
		1,								// w
		0								// アニメーション時間
	);

	tool.RevertEnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_COLOR, 1 /*戻す割合*/, second /*アニメーション時間*/);
	tool.RevertEnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_BG_APPLY, 1 /*戻す割合*/, second /*アニメーション時間*/);
	tool.RevertEnvFadeAnimation(EVENT_LIGHT_ENV_FADE_FOG_DISTANCE, 1 /*戻す割合*/, second /*アニメーション時間*/);
	tool.RevertEnvFadeAnimation(EVENT_LIGHT_ENV_FADE_SKY_COLOR, 1 /*戻す割合*/, second /*アニメーション時間*/);
}

// //
// // 画面が真っ白になる
// //
// void WhiteOut(float second)
// {
// 	EventLightTool light_tool;

// 	light_tool.EnvFadeAnimation(
// 		EVENT_LIGHT_ENV_FADE_FOG_COLOR, // アニメーションさせるパラメータタイプ
// 		2,								// x(r)
// 		2,								// y(g)
// 		2,								// z(b)
// 		1,								// w(a)
// 		second							// アニメーション時間
// 	);
// 	light_tool.EnvFadeAnimation(
// 		EVENT_LIGHT_ENV_FADE_FOG_BG_APPLY, // アニメーションさせるパラメータタイプ
// 		1,								   // x(r)
// 		0,								   // y(g)
// 		0,								   // z(b)
// 		1,								   // w(a)
// 		second							   // アニメーション時間
// 	);
// 	light_tool.EnvFadeAnimation(
// 		EVENT_LIGHT_ENV_FADE_FOG_DISTANCE, // アニメーションさせるパラメータタイプ
// 		-10,							   // x(r)
// 		0,								   // y(g)
// 		0,								   // z(b)
// 		1,								   // w(a)
// 		second							   // アニメーション時間
// 	);
// }

StoryMessageWindow @WhiteOutMessage(float second, float text_vertical_pos = 25)
{
	StoryMessageWindow @window = CreateStoryMessageWindow();

	// メッセージウィンドウの設定
	window.BGColor(1, 1, 1);   // 背景色
	window.FontColor(0, 0, 0); // フォント色
	window.FontBorder(0);	   // フォント縁サイズ
	window.SetLineSpace(10);
	window.TextShowSpeed(1.0f /*表示時間*/);
	window.Show(text_vertical_pos /* 縦位置(%) */, second /*ウィンドウのフェートイン時間*/);

	return window;
}

StoryMessageWindow @BlackOutMessage(float second, float text_vertical_pos = 25)
{
	StoryMessageWindow @window = CreateStoryMessageWindow();

	// メッセージウィンドウの設定
	window.BGColor(0, 0, 0);   // 背景色
	window.FontColor(1, 1, 1); // フォント色
	window.FontBorder(0);	   // フォント縁サイズ
	window.SetLineSpace(10);
	window.TextShowSpeed(1.0f /*表示時間*/);
	window.Show(text_vertical_pos /* 縦位置(%) */, second /*ウィンドウのフェートイン時間*/);

	return window;
}

//===============================================================================
// DLC用アラート関係
UI g_alert_ui;
void Alert_EnemyIncoming()
{
	PlaySe("アラートCAUTION");
	g_alert_ui = CreateUI_File("app:/ui/lyt_HUiMissionMessage.sgo");
}

void Alert_StrongEnemyIncoming()
{
	PlaySe("アラートWARNING");
	g_alert_ui = CreateUI_File("app:/ui/lyt_HUiMissionMessage_danger.sgo");
}

void Wait_Alert()
{
	Wait(5);
}

void Alert_Reinforce()
{
	PlaySe("アラートATTENTION");
	g_alert_ui = CreateUI_File("app:/ui/lyt_HUiMissionMessage_reinforce.sgo");
}

void MissionPack2Startup(string point)
{
	CreateNeutral(point, "app:/object/ev609_VirtualDome.sgo", 1);
}
