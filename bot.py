#@title 🛡️ GUARDIÁN VECINAL PREMIUM (HUARAZ) - MENSAJES INTERNOS MEJORADOS

import sys, subprocess
subprocess.run([sys.executable, "-m", "pip", "install", "python-telegram-bot==20.7 pytz", "-q"], stdout=subprocess.DEVNULL)
import nest_asyncio
nest_asyncio.apply()

import pytz
import asyncio
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, ChatMemberHandler
from telegram.constants import ParseMode
from telegram.error import RetryAfter

TOKEN = "8433052462:AAGjsbQaMdtcBtvcoVwenb5AGIQHLFwa3zU"
TIMEZONE = pytz.timezone("America/Lima")

# ------------------------------------------------------------
# 🎨 TECLADO (NO SE TOCA - IGUAL QUE ANTES)
# ------------------------------------------------------------
def get_main_keyboard():
    keyboard = [
        [InlineKeyboardButton("🔴🚨 ¡ALERTA ROJA! 🚨🔴", callback_data='alerta_roja')],
        [InlineKeyboardButton("👀⚠️ ¡SOSPECHOSO! ⚠️👀", callback_data='sospechoso')],
        [InlineKeyboardButton("🚶‍♂️⚠️ HOMBRE RARO ⚠️🚶‍♂️", callback_data='hombre'),
         InlineKeyboardButton("🚶‍♀️⚠️ MUJER RARA ⚠️🚶‍♀️", callback_data='mujer')],
        [InlineKeyboardButton("🧒😢 NIÑO PERDIDO 😢🧒", callback_data='nino'),
         InlineKeyboardButton("🐕🔍 MASCOTA PERDIDA 🔍🐕", callback_data='mascota')],
        [InlineKeyboardButton("🔥🚒 ¡INCENDIO! 🚒🔥", callback_data='incendio'),
         InlineKeyboardButton("👮📞 SERENAZGO 📞👮", callback_data='serenazgo')],
        [InlineKeyboardButton("📞🆘 EMERGENCIAS 🆘📞", callback_data='emergencias'),
         InlineKeyboardButton("🔊🔔 CONFIGURAR SONIDO 🔔🔊", callback_data='configurar_sonido')],
        [InlineKeyboardButton("📊📈 ESTADÍSTICAS 📈📊", callback_data='stats')]
    ]
    return InlineKeyboardMarkup(keyboard)

# ------------------------------------------------------------
# 🚨 ENVÍO MASIVO CON MENSAJES INTERNOS MEJORADOS
# ------------------------------------------------------------
async def enviar_notificacion_masiva(chat_id, titulo, emoji, usuario, hora, mensaje_base, context, cantidad):
    enviados = 0
    for i in range(1, cantidad + 1):
        progreso = f"{titulo} ({i}/{cantidad})"
        barrera = emoji * 8
        
        mensaje = (
            f"{barrera}\n"
            f"<b>{progreso}</b>\n"
            f"{barrera}\n\n"
            f"🚨 <b>¡ATENCIÓN URGENTE VECINOS!</b> 🚨\n\n"
            f"👤 <b>REPORTA:</b> {usuario}\n"
            f"🕒 <b>HORA:</b> {hora}\n"
            f"━━━━━━━━━━━━━━━━━━━━\n\n"
            f"{mensaje_base}\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"<b>{titulo}</b>\n"
            f"{barrera}\n"
            f"🛡️ <i>Unidos protegemos nuestro barrio</i> 🛡️"
        )
        while True:
            try:
                await context.bot.send_message(chat_id=chat_id, text=mensaje, parse_mode=ParseMode.HTML)
                enviados += 1
                await asyncio.sleep(1.2)
                break
            except RetryAfter as e:
                await asyncio.sleep(e.retry_after)
            except:
                break
    return enviados

# ------------------------------------------------------------
# MENÚ FIJADO (NO SE TOCA)
# ------------------------------------------------------------
async def enviar_y_fijar_menu(chat_id, context):
    msg_text = (
        "🛡️ <b>GUARDIÁN VECINAL · HUARAZ</b> 🛡️\n\n"
        "👇 <b>TOCA AQUÍ PARA LOS BOTONES</b> 👇\n\n"
        "📌 <i>Mensaje fijado · Siempre visible</i>"
    )
    try:
        msg = await context.bot.send_message(chat_id=chat_id, text=msg_text, reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)
        await msg.pin(disable_notification=True)
    except:
        pass

async def on_chat_member_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.my_chat_member and update.my_chat_member.new_chat_member.status == "member":
        await enviar_y_fijar_menu(update.my_chat_member.chat.id, context)

# ------------------------------------------------------------
# COMANDOS
# ------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🛡️ <b>GUARDIÁN ACTIVO</b> 🛡️", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 <b>PANEL DE ALERTAS</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

async def menu_corto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await menu_command(update, context)

async def fijar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id, user_id)
        if member.status in ['administrator', 'creator']:
            await enviar_y_fijar_menu(chat_id, context)
            await update.message.reply_text("✅ <b>MENÚ FIJADO</b>", parse_mode=ParseMode.HTML)
        else:
            await update.message.reply_text("❌ SOLO ADMINISTRADORES")
    except:
        await update.message.reply_text("❌ ERROR")

async def emergencia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "📞 <b>EMERGENCIAS HUARAZ</b>\n\n"
        "🚔 105 / (043) 42-1330\n"
        "🚑 106\n"
        "🔥 116 / (043) 42-3333\n"
        "🏥 (043) 42-1861\n"
        "🛡️ (043) 42-7700\n"
        "💡 0801 71001\n"
        "💧 (043) 42-1401"
    )
    await update.message.reply_text(texto, parse_mode=ParseMode.HTML, reply_markup=get_main_keyboard())

async def enviar_instrucciones_sonido(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    texto = (
        "🔊 <b>SONIDO DE ALERTA</b>\n\n"
        "1️⃣ Toca el nombre del grupo\n"
        "2️⃣ Notificaciones\n"
        "3️⃣ Sonido personalizado\n"
        "4️⃣ Elige tono FUERTE\n\n"
        "✅ ¡LISTO!"
    )
    await query.edit_message_text(text=texto, reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

# ------------------------------------------------------------
# 🔥 PROCESADOR DE BOTONES - MENSAJES INTERNOS MEJORADOS 🔥
# ------------------------------------------------------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user = query.from_user.full_name
    chat_id = query.message.chat_id
    hora = datetime.now(TIMEZONE).strftime("%I:%M %p")
    data = query.data

    await query.edit_message_text("⏳ <b>ACTIVANDO ALERTA...</b>", reply_markup=None, parse_mode=ParseMode.HTML)

    if data == 'alerta_roja':
        titulo = "🚨 ¡PELIGRO INMINENTE! 🚨"
        emoji = "🔴"
        mensaje = (
            f"🔥🔥 <b>¡ALERTA MÁXIMA VECINAL!</b> 🔥🔥\n\n"
            f"⚠️⚠️ <b>¡ROBO O DELITO EN CURSO!</b> ⚠️⚠️\n\n"
            f"🏠 <b>¡SALGAN DE SUS CASAS CON PRECAUCIÓN!</b>\n"
            f"📢 <b>¡HAGAN RUIDO! ¡ENCIENDAN LUCES!</b>\n"
            f"👥 <b>¡REÚNANSE CON OTROS VECINOS!</b>\n"
            f"🚫 <b>¡NO ENFRENTEN SOLOS AL DELINCUENTE!</b>\n\n"
            f"📞📞 <b>¡LLAMEN AL 105 Y SERENAZGO YA!</b> 📞📞\n\n"
            f"📍 <b>UBÍQUENSE EN PUNTOS ESTRATÉGICOS</b>\n"
            f"📸 <b>TOMEN FOTOS COMO EVIDENCIA</b>\n\n"
            f"📹 <b>VIDEOLLAMADA GRUPAL ACTIVA</b> 📹\n"
            f"👉 <i>Toca el ícono de cámara arriba</i>"
        )
        try:
            await context.bot.create_video_chat(chat_id)
        except:
            pass
        try:
            await context.bot.send_dice(chat_id=chat_id, emoji='🎯')
            await context.bot.send_dice(chat_id=chat_id, emoji='🔥')
            await context.bot.send_dice(chat_id=chat_id, emoji='💣')
        except:
            pass
        enviados = await enviar_notificacion_masiva(chat_id, titulo, emoji, user, hora, mensaje, context, 100)
        await query.edit_message_text(f"✅ <b>¡ALERTA ROJA {enviados}/100!</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

    elif data == 'sospechoso':
        titulo = "⚠️ ¡ACTITUD SOSPECHOSA! ⚠️"
        emoji = "🟡"
        mensaje = (
            f"👀👀 <b>¡PERSONA SOSPECHOSA EN LA ZONA!</b> 👀👀\n\n"
            f"🚶‍♂️🚶‍♀️ <b>Está merodeando sin rumbo claro</b>\n"
            f"🏘️ <b>Observa casas y vehículos</b>\n\n"
            f"💡 <b>¡VECINOS ENCIENDAN LUCES EXTERIORES!</b>\n"
            f"📸 <b>Si es seguro, tomen foto y compartan</b>\n"
            f"👮 <b>Reporten a Serenazgo si persiste</b>\n\n"
            f"⚠️ <b>¡NO CONFRONTEN! SOLO OBSERVEN</b> ⚠️"
        )
        enviados = await enviar_notificacion_masiva(chat_id, titulo, emoji, user, hora, mensaje, context, 30)
        await query.edit_message_text(f"✅ <b>{enviados}/30</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

    elif data == 'hombre':
        titulo = "🚶‍♂️ ¡HOMBRE SOSPECHOSO! 🚶‍♂️"
        emoji = "🟠"
        mensaje = (
            f"👤👤 <b>¡HOMBRE SOSPECHOSO AVISTADO!</b> 👤👤\n\n"
            f"🚶‍♂️ <b>Merodea mirando casas y vehículos</b>\n"
            f"🏘️ <b>Actitud sospechosa en el barrio</b>\n\n"
            f"💡 <b>¡VECINOS ENCIENDAN LUCES!</b>\n"
            f"📍 <b>Indiquen ubicación exacta si lo ven</b>\n"
            f"📢 <b>Avisen a otros vecinos</b>\n\n"
            f"🛑 <b>¡NO ABRAN LA PUERTA A DESCONOCIDOS!</b> 🛑"
        )
        enviados = await enviar_notificacion_masiva(chat_id, titulo, emoji, user, hora, mensaje, context, 30)
        await query.edit_message_text(f"✅ <b>{enviados}/30</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

    elif data == 'mujer':
        titulo = "🚶‍♀️ ¡MUJER SOSPECHOSA! 🚶‍♀️"
        emoji = "🟠"
        mensaje = (
            f"👤👤 <b>¡MUJER SOSPECHOSA AVISTADA!</b> 👤👤\n\n"
            f"🚶‍♀️ <b>Toca timbres con excusas</b>\n"
            f"🏘️ <b>Observa propiedades detenidamente</b>\n\n"
            f"📍 <b>Compartan ubicación si la ven</b>\n"
            f"📸 <b>Tomen foto discreta si es posible</b>\n"
            f"📢 <b>Avisen a los vecinos</b>\n\n"
            f"🛑 <b>¡NO ABRAN LA PUERTA NI DEN DATOS!</b> 🛑"
        )
        enviados = await enviar_notificacion_masiva(chat_id, titulo, emoji, user, hora, mensaje, context, 30)
        await query.edit_message_text(f"✅ <b>{enviados}/30</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

    elif data == 'nino':
        titulo = "😢 ¡NIÑO PERDIDO! 😢"
        emoji = "🔵"
        mensaje = (
            f"🧒🧒 <b>¡UN NIÑO ESTÁ PERDIDO EN EL BARRIO!</b> 🧒🧒\n\n"
            f"😟 <b>{user} necesita nuestra ayuda</b>\n\n"
            f"🏡 <b>¡VECINOS REVISEN!</b>\n"
            f"🌳 Jardines y patios\n"
            f"🚗 Debajo de carros\n"
            f"🏠 Garajes y esquinas\n\n"
            f"📢 <b>Si lo encuentran:</b>\n"
            f"✅ Manténganlo seguro\n"
            f"✅ Avisen INMEDIATO al grupo\n"
            f"✅ Contacten a {user}\n\n"
            f"❤️❤️ <b>¡GRACIAS POR AYUDAR!</b> ❤️❤️"
        )
        enviados = await enviar_notificacion_masiva(chat_id, titulo, emoji, user, hora, mensaje, context, 30)
        await query.edit_message_text(f"✅ <b>{enviados}/30</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

    elif data == 'mascota':
        titulo = "🐕 ¡MASCOTA PERDIDA! 🐕"
        emoji = "🟢"
        mensaje = (
            f"🐾🐾 <b>¡MASCOTA PERDIDA EN EL BARRIO!</b> 🐾🐾\n\n"
            f"🐕 <b>{user} necesita tu ayuda</b>\n\n"
            f"👀 <b>¡VECINOS ESTÉN ATENTOS!</b>\n"
            f"📸 Si la ven, tomen FOTO\n"
            f"🏷️ Revisen si tiene PLACA\n"
            f"📍 Indiquen UBICACIÓN exacta\n\n"
            f"⚠️ <b>NO LA PERSIGAN</b> si es asustadiza\n"
            f"📢 Solo avisen al grupo\n\n"
            f"❤️ <b>¡GRACIAS POR COLABORAR!</b> ❤️"
        )
        enviados = await enviar_notificacion_masiva(chat_id, titulo, emoji, user, hora, mensaje, context, 30)
        await query.edit_message_text(f"✅ <b>{enviados}/30</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

    elif data == 'incendio':
        texto = (
            f"🔥🔥🔥 <b>¡INCENDIO! ¡INCENDIO!</b> 🔥🔥🔥\n\n"
            f"🚒🚒🚒🚒🚒🚒🚒🚒🚒🚒\n\n"
            f"👤 <b>{user} reporta FUEGO</b>\n\n"
            f"📞📞 <b>¡LLAMEN YA!</b> 📞📞\n"
            f"🚒 <b>BOMBEROS:</b> 116 / (043) 42-3333\n\n"
            f"🚪 <b>¡EVACÚEN CON CALMA!</b>\n"
            f"⬇️ Agáchense (el humo sube)\n"
            f"🧯 Usen extintor si es seguro\n"
            f"🏃 Alejados del fuego\n\n"
            f"⚠️⚠️ <b>¡NO SE ARRIESGUEN POR OBJETOS!</b> ⚠️⚠️\n\n"
            f"📢 Avisen a vecinos cercanos"
        )
        await context.bot.send_message(chat_id=chat_id, text=texto, parse_mode=ParseMode.HTML)
        await query.edit_message_text("✅ <b>ALERTA ENVIADA</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

    elif data == 'serenazgo':
        texto = (
            f"👮👮 <b>¡CONTACTAR A SERENAZGO!</b> 👮👮\n\n"
            f"🚔🚔🚔🚔🚔🚔🚔🚔🚔🚔\n\n"
            f"👤 <b>{user} solicita reportar</b>\n\n"
            f"📞📞 <b>¡LLAMEN AHORA!</b> 📞📞\n\n"
            f"🏘️ <b>SERENAZGO HUARAZ:</b>\n"
            f"📞 (043) 42-7700\n"
            f"📞 (043) 42-9955\n\n"
            f"🏘️ <b>SERENAZGO INDEPENDENCIA:</b>\n"
            f"📞 (043) 39-6262\n"
            f"📞 943 999 270\n\n"
            f"📝 <b>Al reportar:</b>\n"
            f"✅ Dirección exacta\n"
            f"✅ Descripción de la situación\n"
            f"✅ Mantengan la calma\n\n"
            f"🤝 <b>¡UNIDOS SOMOS MÁS FUERTES!</b> 🤝"
        )
        await context.bot.send_message(chat_id=chat_id, text=texto, parse_mode=ParseMode.HTML)
        await query.edit_message_text("✅ <b>INFO ENVIADA</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

    elif data == 'stats':
        try:
            count = await context.bot.get_chat_member_count(chat_id)
        except:
            count = "—"
        await query.edit_message_text(
            f"📊 <b>ESTADÍSTICAS DEL GRUPO</b> 📊\n\n"
            f"👥👥👥👥👥👥👥👥\n\n"
            f"🏘️ <b>VECINOS CONECTADOS:</b>\n"
            f"👤 <b>{count}</b> PERSONAS\n\n"
            f"🕒 <b>ÚLTIMA ALERTA:</b>\n"
            f"⏰ {hora}\n\n"
            f"🛡️🛡️ <b>BOT ACTIVO 24/7</b> 🛡️🛡️",
            reply_markup=get_main_keyboard(),
            parse_mode=ParseMode.HTML
        )

    elif data == 'emergencias':
        texto = (
            f"📞🆘 <b>DIRECTORIO DE EMERGENCIAS</b> 🆘📞\n\n"
            f"🏥🏥🏥🏥🏥🏥🏥🏥🏥🏥\n\n"
            f"🚔 <b>POLICÍA NACIONAL</b>\n"
            f"📞 <b>105</b> (Emergencia)\n"
            f"📞 (043) 42-1330 (Comisaría)\n\n"
            f"🚑 <b>SAMU - AMBULANCIAS</b>\n"
            f"📞 <b>106</b>\n\n"
            f"🔥 <b>BOMBEROS</b>\n"
            f"📞 <b>116</b> (Emergencia)\n"
            f"📞 (043) 42-3333\n\n"
            f"🏥 <b>HOSPITAL V.R. GUARDIA</b>\n"
            f"📞 (043) 42-1861\n"
            f"📞 (043) 42-7120\n\n"
            f"🏥 <b>ESSALUD HUARAZ</b>\n"
            f"📞 (043) 42-2919\n\n"
            f"🏥 <b>CLÍNICA SAN PABLO</b>\n"
            f"📞 (043) 42-1698\n\n"
            f"🛡️ <b>SERENAZGO HUARAZ</b>\n"
            f"📞 (043) 42-7700\n\n"
            f"💡 <b>HIDRANDINA (LUZ)</b>\n"
            f"📞 0801 71001\n\n"
            f"💧 <b>EPS CHAVÍN (AGUA)</b>\n"
            f"📞 (043) 42-1401\n\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"⛑️ <b>GUARDA ESTE MENSAJE</b> ⛑️"
        )
        await context.bot.send_message(chat_id=chat_id, text=texto, parse_mode=ParseMode.HTML)
        await query.edit_message_text("✅ <b>DIRECTORIO ENVIADO</b>", reply_markup=get_main_keyboard(), parse_mode=ParseMode.HTML)

    elif data == 'configurar_sonido':
        await enviar_instrucciones_sonido(update, context)

# ------------------------------------------------------------
# ARRANQUE
# ------------------------------------------------------------
async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(ChatMemberHandler(on_chat_member_update, ChatMemberHandler.MY_CHAT_MEMBER))
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", menu_command))
    app.add_handler(CommandHandler("m", menu_corto))
    app.add_handler(CommandHandler("fijar", fijar_menu))
    app.add_handler(CommandHandler("emergencia", emergencia_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("🤖 GUARDIÁN VECINAL ACTIVO - MENSAJES MEJORADOS")
    await app.run_polling(allowed_updates=Update.ALL_TYPES)

await main()
