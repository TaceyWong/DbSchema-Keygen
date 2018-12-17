package main

import (
	"crypto/md5"
	"encoding/hex"
	"math/rand"
	"strconv"
	"time"

	"github.com/andlabs/ui"
	_ "github.com/andlabs/ui/winmanifest"
)

func genKey(name string) string {
	r := rand.New(rand.NewSource(time.Now().UnixNano()))
	salt := strconv.Itoa(r.Intn(20000) + 10000)
	saltedText := "ax5" + name + "b52w" + salt + "vb3"
	hasher := md5.New()
	hasher.Write([]byte(saltedText))
	hashedText := hex.EncodeToString(hasher.Sum(nil))
	resultKey := hashedText[:4] + salt + hashedText[4:]
	return resultKey
}

func setup() {
	mainwin := ui.NewWindow("DbSchema序列号生成器", 400, 140, true)

	mainwin.OnClosing(func(*ui.Window) bool {
		ui.Quit()
		return true
	})
	ui.OnShouldQuit(func() bool {
		mainwin.Destroy()
		return true
	})

	vbox := ui.NewVerticalBox()
	vbox.SetPadded(true)
	mainwin.SetChild(vbox)

	group := ui.NewGroup("")
	group.SetMargined(true)
	vbox.Append(group, true)

	group.SetChild(ui.NewNonWrappingMultilineEntry())

	entryForm := ui.NewForm()
	entryForm.SetPadded(true)
	group.SetChild(entryForm)
	user := ui.NewEntry()
	entryForm.Append("注册名", user, false)
	vbox.Append(ui.NewHorizontalSeparator(), false)

	genBtn := ui.NewButton("生成序列号")
	vbox.Append(genBtn, false)

	result := ui.NewEntry()
	result.SetReadOnly(true)
	entryForm.Append("序列号", result, false)
	result.SetText("在上方随便输入注册名，点击下方按钮生成")
	vbox.Append(ui.NewHorizontalSeparator(), false)

	genBtn.OnClicked(func(*ui.Button) {
		if user.Text() == "" {
			ui.MsgBoxError(mainwin,
				"用户名错误",
				"用户名不能为空")
		} else {
			key := genKey(user.Text())
			ui.MsgBox(mainwin, "成功生成", "请复制注册名和序列号进行软件激活:\n菜单栏->HELP->Register->输入激活")
			result.SetText(key)
		}
	})

	mainwin.Show()

}

func main() {

	ui.Main(setup)
}
