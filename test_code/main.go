package main
// 那来压测的客户端
import (
	"bytes"
	"encoding/binary"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"math/rand"
	"net"
	"sync"
	"time"
)

// ====================================

type Message struct {
	DataLen int32
	MsgType int32
	Data	[]byte
}

func NewMessage(msgType int32, data []byte) *Message {
	dataLen := len(data)
	return &Message{
		DataLen:int32(dataLen),
		MsgType:msgType,
		Data:data,
	}
}

func(m *Message) GetDataLen() int32 {
	return m.DataLen
}

func(m *Message) GetMsgType() int32 {
	return m.MsgType
}

func(m *Message) GetData() []byte {
	return m.Data
}

func(m *Message) SetDataLen(dataLen int32) {
	m.DataLen = dataLen
}

func(m *Message) SetMsgType(dataType int32) {
	m.MsgType = dataType
}

func(m *Message) SetData(data []byte) {
	m.Data = data
}

func(m *Message) ShowData() {
	fmt.Printf("len = %d, type = %d msg = ", m.GetDataLen(), m.GetMsgType())
	for _, v := range m.GetData() {
		fmt.Printf("%c", v)
	}
	fmt.Println()
}

// =========================================

type Serializable struct {}

func NewSerializable() *Serializable {
	return &Serializable{}
}

func (s *Serializable) GetSerializeMsg(conn *net.TCPConn) (*Message, error) {
	headData  := make([]byte, s.GetHeadLen())
	if _, err := io.ReadFull(conn, headData); err != nil {
		return nil, errors.New(fmt.Sprintln("read msg head error", err))
	}
	msg, err := s.deSerializationHead(headData)
	if err != nil {
		return nil, errors.New(fmt.Sprintln("De serialize error ", err))
	}
	var data []byte
	if msg.GetDataLen() > 0 && msg.GetDataLen() < 10240 {
		data = make([]byte, msg.GetDataLen())
		if _, err := io.ReadFull(conn, data); err != nil {
			return nil, errors.New(fmt.Sprintln("read msg body error ", err))
		}
	}
	msg.SetData(data)
	return msg, nil
}

func (s *Serializable) Serialize(msg *Message) ([]byte, error) {
	dataBuff := bytes.NewBuffer([]byte{})
	if err := binary.Write(dataBuff, binary.BigEndian, msg.GetDataLen()); err != nil {
		return nil, err
	}
	if err := binary.Write(dataBuff, binary.BigEndian, msg.GetMsgType()); err != nil {
		return nil, err
	}
	if err := binary.Write(dataBuff, binary.BigEndian, msg.GetData()); err != nil {
		return nil ,err
	}
	return dataBuff.Bytes(), nil
}

func (s *Serializable) deSerializationHead(binaryData []byte) (*Message, error) {
	dataBuff := bytes.NewReader(binaryData)
	msg := &Message{}
	if err := binary.Read(dataBuff, binary.BigEndian, &msg.DataLen); err != nil {
		return nil, err
	}
	if err := binary.Read(dataBuff, binary.BigEndian, &msg.MsgType); err != nil {
		return nil, err
	}
	return msg, nil
}

func (s *Serializable) GetHeadLen() int32 {
	return 8
}

// =========================================================================

type RequestContent struct {
	LastTime int32 `json:"last_time"`
	Msg string	`json:"msg"`
}

type ResponseContent struct {
	Ret int32 `json:"ret"`
	ErrMsg string `json:"err_msg"`
	LastTime int32 `json:"last_time"`
	Extend string `json:"extend"`
}

func echoOnce(cnt int, ch chan int) {
	// 117.78.5.122
	conn, err := net.Dial("tcp", "117.78.5.122:7736")
	if err != nil{
		fmt.Println("client dial err:", err)
		return
	}
	rnd := rand.Intn(100)
	time.Sleep(time.Duration(rnd) * time.Millisecond)
	// request
	for i := 1; i <= cnt; i++ {
		rnd = rand.Intn(100)
		time.Sleep(time.Duration(rnd) * time.Millisecond)
		//time.Sleep(66 * time.Millisecond)
		nowTime := int32(time.Now().UnixNano() / 1e6)
		req := RequestContent{ nowTime, ""}
		buffer, err := json.Marshal(req)

		if err != nil {
			fmt.Println("json parse fail.")
			return
		}

		msg := NewMessage(666, []byte(buffer))
		ser := NewSerializable()
		data, err := ser.Serialize(msg)
		if err != nil {
			fmt.Println("Serialize msg fail")
			return
		}
		_, err = conn.Write(data)
		if err != nil {
			fmt.Println("connect write data err")
			return
		}

		resMsg, err := ser.GetSerializeMsg(conn.(*net.TCPConn))

		if err != nil {
			fmt.Println("get msg from net error")
			return
		}
		//resMsg.ShowData()

		buffer, err = ser.Serialize(resMsg)

		if err != nil {
			fmt.Println("serialize fail")
			return
		}

		var res ResponseContent
		err = json.Unmarshal(resMsg.GetData(), &res)
		if err != nil {
			fmt.Println("response parse fail.")
			return
		}
		nowTime = int32(time.Now().UnixNano() / 1e6)
		cut_time := nowTime - res.LastTime
		//fmt.Println(cut_time)
		mutex.Lock()

		//cut_time /= 100

		if cut_time > 2000 {
			count[2000] += 1
		} else {
			count[cut_time] += 1
		}
		mutex.Unlock()
	}
	_ = conn.Close()
	ch <- 1
}

var mutex sync.Mutex
var count = make([]int, 2005)
var result = make(chan int)

func main() {

	rand.Seed(time.Now().UnixNano())

	limit := 50

	for i := 1; i <= limit; i++ {
		go echoOnce(20, result)
	}

	var cnt int
	var sum int = 0
	var enough bool = false
	for {
		select {
			case cnt = <-result:
				sum += cnt
				if sum >= limit {
					enough = true
				}
		}
		if enough {
			break
		}
	}
	for i := 0; i <= 2000; i++ {
		if count[i] > 0 {
			fmt.Printf("%d %d\n", i, count[i])
		}
	}

}
