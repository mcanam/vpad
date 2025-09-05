const stateData = { 
    btn_dpad_up: false,
    btn_dpad_down: false,
    btn_dpad_left: false,
    btn_dpad_right: false,
    btn_y: false, 
    btn_x: false, 
    btn_b: false, 
    btn_a: false, 
    btn_tl: false,
    btn_tr: false,
    btn_start: false,
    btn_select: false,
    abs_z: 0,
    abs_rz: 0,
    abs_x: 0, 
    abs_y: 0, 
    abs_rx: 0, 
    abs_ry: 0
};

const socket = new WebSocket(window.location.origin + '/ws');
let isConnected = false;

socket.onopen = () => {
    isConnected = true;
    console.log('socket connected.');
};

socket.onclose = () => {
    isConnected = false;
    console.log('socket disconnected.');
}

socket.onmessage = ({ data }) => {
    // do something
}

socket.onerror = error => {
    // do something
}

function sendData() {
    isConnected && socket.send(JSON.stringify(stateData));
}

const $startContainer = document.querySelector('.start-container');
const $startButton = document.querySelector('.start-button');
const $buttons = document.querySelectorAll('[data-key]');
const $thumbstickLeftContainer = document.querySelector('.thumbstick-container-left');
const $thumbstickRightContainer = document.querySelector('.thumbstick-container-right');

$startButton.addEventListener('click', () => {
    document.body.requestFullscreen();
    screen.orientation.lock('landscape-secondary');
    $startContainer.style.display = 'none';
});

$buttons.forEach($button => {
    const key = $button.dataset.key;

    $button.addEventListener('touchstart', () => {
        stateData[key] = (key == 'abs_z' || key == 'abs_rz') ? 255 : 1;
        sendData();
        $button.classList.add('button-active');
    });

    $button.addEventListener('touchend', () => {
        stateData[key] = 0;
        sendData();
        $button.classList.remove('button-active');
    });
});

const thumbstickLeft = nipplejs.create({
    zone: $thumbstickLeftContainer,
    mode: 'static',
    size: 60,
    position: { left: '50%', top: '50%' },
});

const thumbstickRight = nipplejs.create({
    zone: $thumbstickRightContainer,
    mode: 'static',
    size: 60,
    position: { left: '50%', top: '50%' },
});

function getThumbstickPosition(data) {
    const angleDeg = data.angle.degree;
    const force = Math.min(data.force, 1);
    const angleRad = angleDeg * Math.PI / 180;
    const absX = Math.round(128 + force * 128 * Math.cos(angleRad));
    const absY = Math.round(128 - force * 128 * Math.sin(angleRad));

    return {
        x: Math.min(Math.max(absX, 0), 255),
        y: Math.min(Math.max(absY, 0), 255)
    };
}

thumbstickLeft.on('move', (_, data) => {
    const { x, y } = getThumbstickPosition(data);

    stateData.abs_x = x;
    stateData.abs_y = y;

    sendData();
});

thumbstickRight.on('move', (_, data) => {
    const { x, y } = getThumbstickPosition(data);

    stateData.abs_rx = x;
    stateData.abs_ry = y;

    sendData();
});

thumbstickLeft.on('end', () => {
    stateData.abs_x = 128;
    stateData.abs_y = 128;

    sendData();
});

thumbstickRight.on('end', () => {
    stateData.abs_rx = 128;
    stateData.abs_ry = 128;

    sendData();
});
