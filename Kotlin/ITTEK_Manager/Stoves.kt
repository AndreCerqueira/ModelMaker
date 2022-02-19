package com.ittekpremium.ittekmanager.Models

import org.json.JSONObject

class Stoves 
{
	//Variables
	var id: Int? = null
	var stove_number: Int? = null
	var active: Boolean? = null

	constructor(){ 
	}

	constructor(
		id: Int, 
		stove_number: Int, 
		active: Boolean, 
	){
		this.id = id
		this.stove_number = stove_number
		this.active = active
	}

	fun toJson(): JSONObject { 
	
		val jsonObject = JSONObject()

		jsonObject.put("id", id)
		jsonObject.put("stove_number", stove_number)
		jsonObject.put("active", active)

		return jsonObject
	}

	companion object {
		fun fromJson(jsonObject: JSONObject) : Stoves { 	
			val stoves = Stoves()

			stoves.id = if (!jsonObject.isNull("id")) jsonObject.getInt("id") else null
			stoves.stove_number = if (!jsonObject.isNull("stove_number")) jsonObject.getInt("stove_number") else null
			stoves.active = if (!jsonObject.isNull("active")) jsonObject.getBoolean("active") else null

			return stoves
		}
	}

}