async function hash(msg,salt){
    msg = string_to_buffer(msg);
    salt = string_to_buffer(salt);
    let space_cost = 1024;
    let time_cost = 3;
    let dependencies = 3;
    let msg_hash = await balloon_hash(msg,salt,space_cost,time_cost,dependencies);
    msg_hash = buffer_to_hex(msg_hash);
    return msg_hash;
}

async function balloon_hash(msg,salt,space_cost,time_cost,dependencies){
    let count = 0;
    let main_buffer = [];
    
    main_buffer[0] = await sha256(count,msg,salt);
    count += 1;
    for (let space_i=1; space_i < space_cost; space_i++) {
        main_buffer[space_i] = await sha256(count,main_buffer[space_i-1]);
        count += 1;
    }
    
    for (let time_i=0; time_i < time_cost; time_i++) {
        for (let space_i=0; space_i < space_cost; space_i++) {
            if (space_i===0){
                main_buffer[space_i] = await sha256(count,main_buffer[space_cost-1],main_buffer[space_i]);
            } else {
                main_buffer[space_i] = await sha256(count,main_buffer[space_i-1],main_buffer[space_i]);
            }
            count += 1;
            for (let dependency_i=0; dependency_i < dependencies; dependency_i++){
                index_block = await sha256(time_i,space_i,dependency_i);
                other_space_i = buffer_to_int(await sha256(count,salt,index_block)).mod(space_cost).valueOf();
                count += 1;
                main_buffer[space_i] = await sha256(count,main_buffer[space_i],main_buffer[other_space_i]);
                count += 1;
            }
        }
    }
    
    return main_buffer[space_cost-1];
}

async function sha256() {
    let t = new Uint8Array(0);
    for (let i = 0; i < arguments.length; i++) {
        let value = arguments[i];
        if (Number.isInteger(value)) {value = int_to_buffer(value,8);}
        if (typeof value === 'string') {value = string_to_buffer(value);}
        t = concat_buffers(t,value);
    }
    return await window.crypto.subtle.digest("SHA-256",t);
}

function buffer_to_hex(buffer) {
    return [...new Uint8Array (buffer)]
        .map (b => b.toString (16).padStart (2, "0"))
        .join ("");
}
function buffer_to_hex_rev(buffer) {
    return [...new Uint8Array (buffer)]
        .map (b => b.toString (16).padStart (2, "0"))
        .reverse()
        .join ("");
}

function buffer_to_int(buffer) {
    buffer = buffer_to_hex_rev(buffer);
    return bigInt(buffer,16);
}

function string_to_buffer(msg) {
    let encoder = new TextEncoder("utf-8");
    return encoder.encode(msg);
}

function int_to_buffer(value,length) {
    const view = new DataView(new ArrayBuffer(length))
    for (var index = 0; index < length; index++) {
        if (Number.isInteger(value)) {
            view.setUint8(index, value % 256)
            value = value >> 8;
        }
        else {
            let result = value.divmod(256);
            view.setUint8(index, result.remainder.valueOf())
            value = result.quotient;
        }
    }
    return view.buffer
}

function hex_to_buffer(value) {
    const view = new DataView(new ArrayBuffer(value.length/2))
    for (var index = 0; index < value.length/2; index++) {
        let int_value = parseInt(value[index*2]+value[index*2+1],16);
      view.setUint8(index, int_value)
    }
    return view.buffer
}

function concat_buffers( buffer1, buffer2 ) {
  let new_buffer = buffer_to_hex(buffer1)+buffer_to_hex(buffer2);
  return hex_to_buffer(new_buffer);
}
